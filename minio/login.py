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
from env import MINIOHOST, MINIOUSER, MINIOTOKEN

from minio import Minio

def login_minio():
    client = Minio(
        MINIOHOST, access_key=MINIOUSER, secret_key=MINIOTOKEN, secure=False,
    )
    return client
