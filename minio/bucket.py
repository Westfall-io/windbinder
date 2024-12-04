# Copyright (c) 2023-2024 Westfall Inc.
#
# This file is part of Windbinder.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, and can be found in the file NOTICE inside this
# git repository.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from env import VOLUME, MINIORETENTIONDAYS

import shutil

from datetime import datetime, timedelta

from minio.error import S3Error
from minio.commonconfig import GOVERNANCE, Tags
from minio.retention import Retention

def parse_bucket_name(qualifiedName):
    bucket = qualifiedName.lower().strip().replace('_', '-'). \
        replace("'", "").replace('"', "").replace("\\","").replace("/",""). \
        replace("::", ".").replace(" ","-")

    if len(bucket) > 63:
        bucket = bucket[:63]
    elif len(bucket) < 3:
        bucket = bucket+'-bucket'

    return bucket

def download_dependent_output(client, action_prev, prev_thread_name):
    bucket = parse_bucket_name(action_prev["qualifiedName"])
    print('Downloading and unzipping prior dependency output.')
    client.fget_object(bucket,"output-"+prev_thread_name+".zip", "output"+prev_thread_name+".zip")

    # Overwrite the base image with output from the dependency, we'll
    # overwrite with new input after this step
    shutil.unpack_archive("output-"+prev_thread_name+".zip", VOLUME, "zip")

def create_bucket(client, action, thread_name, name='input', tmp_location='tmp'):
    # Make an archive of the input bucket
    print('Making an archive for storage from directory: {}.'.format(tmp_location))
    fname = name+'-'+thread_name

    # Print all files being zipped
    import os
    file_list=os.listdir(VOLUME)
    print(file_list)
    file_list=os.listdir(tmp_location)
    print(file_list)

    shutil.make_archive(fname, 'zip', tmp_location)

    # Create a retention date
    retention_date = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0,
    ) + timedelta(days=MINIORETENTIONDAYS)

    # Tag it as the named bucket (either input or output typically)
    tags = Tags(for_object=True)
    tags["type"] = name

    print('Uploading to Minio')
    # Get the bucket
    bucket = parse_bucket_name(action["qualifiedName"])
    try:
        # Make a bucket if needed
        found = client.bucket_exists(bucket)
        if not found:
            client.make_bucket(bucket, object_lock=True)
            print("Bucket made!")
        else:
            print("Bucket already exists!")
    except S3Error as exc:
        print("error occurred.", exc)

    print("Uploading file name: {}".format(fname+".zip"))
    try:
        # Upload
        client.fput_object(
            bucket, fname+'.zip', fname+'.zip',
            tags=tags,
            retention=Retention(GOVERNANCE, retention_date)
        )
    except S3Error as exc:
        print("error occurred.", exc)
