# Copyright (c) 2023-2024 Westfall Inc.
#
# This file is part of Windbound.
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
        replace("::", ".")

    if len(bucket) > 63:
        bucket = bucket[:63]
    elif len(bucket) < 3:
        bucket = bucket+'-bucket'

    return bucket

def download_dependent_output(client, action_prev):
    bucket = parse_bucket_name(action_prev["qualifiedName"])
    print('Downloading and unzipping prior dependency output.')
    client.fget_object(bucket,"output"+prev_thread_name+".zip", "output"+prev_thread_name+".zip")

    # Overwrite the base image with output from the dependency, we'll
    # overwrite with new input after this step
    shutil.unpack_archive("output"+prev_thread_name+".zip", VOLUME, "zip")

def create_input_bucket(client, action):
    # Make an archive of the input bucket
    print('Making an archive for storage.')
    shutil.make_archive('input'+thread_name, 'zip', 'tmp')

    print('Uploading to Minio')
    try:
        # Get the bucket
        bucket = parse_bucket_name(action["qualifiedName"])
        found = client.bucket_exists(bucket)
        if not found:
            client.make_bucket(bucket, object_lock=True)
            print("Bucket made!")
        else:
            print("Bucket already exists!")

        # Create a retention date
        retention_date = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0,
        ) + timedelta(days=MINIORETENTIONDAYS)

        # Tag it as an input type bucket
        tags = Tags(for_object=True)
        tags["type"] = "input"

        # Upload
        client.fput_object(
            bucket, 'input'+thread_name+'.zip', 'input'+thread_name+'.zip',
            tags=tags,
            retention=Retention(GOVERNANCE, retention_date)
        )

        # Check if we can download the file
        #objects = client.list_objects(bucket)
        #for item in client.list_objects(bucket,recursive=True):
        #    client.fget_object(bucket,item.object_name,'inputdl.zip')

    except S3Error as exc:
        print("error occurred.", exc)
