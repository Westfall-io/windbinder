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
from env import *

import base64
import requests

def login_windstorm_api():
    client_id = WINDSTORMAPICLIENT
    client_secret = WINDSTORMAPISECRET

    # Encode the client ID and client secret
    authorization = base64.b64encode(
        bytes(client_id + ":" + client_secret, "ISO-8859-1")
    ).decode("ascii")

    headers = {
        "Authorization": f"Basic {authorization}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {
        "grant_type": "client_credentials"
    }

    url = KEYCLOAKHOST + '/realms/' + \
          KEYCLOAMREALM + '/protocol/openid-connect/auth'

    r = requests.post(url, data=body, headers=headers)
    token_raw = json.loads(r.text)
    token = token_raw["access_token"]
    return token
