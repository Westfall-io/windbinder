# Copyright (c) 2023-2024 Westfall Inc.
#
# This file is part of Windrunner.
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
from env import WINDSTORMAPIHOST, VOLUME

import os

import requests

from jinja2 import Template

def update_thread_status(token, thread_execution_id, status):
    print('Updating thread execution {} status'.format(thread_execution_id))
    r = requests.put(
        WINDSTORMAPIHOST+"auth/update_thread/{}".format(
            thread_execution_id
        ), json ={'status':status}
    )

    if r.status_code != 200:
        print('Failed to update status')
        thread_name = ''
    else:
        thread_name = r.json()['name']

    return thread_name

def fix_null_issue(action):
    if action['dependency'] == 'null':
        action['dependency'] = None
    return action

def check_thread_dependency(action, prev_thread_name):
    print('Running workflow prep for action: {}--{}'.format(
        action['id'],action['qualifiedName']
    ))

    # Change null to None
    action = fix_null_issue(action)

    if action['dependency'] is None:
        # This action has no dependencies.
        return None

    # This is a dependent action.
    r = requests.get(
        WINDSTORMAPIHOST+"models/threads/thread/{}?validate=false".format(
            action['dependency']
        )
    )

    # Get dependency name
    try:
        action_prev = r.json()['results'][0]
    except:
        try:
            print(r.json())
            raise NotImplementedError('Could not find action to pull output data from.')
        except:
            print(r.request.url)
            print(r.request.body)
            print(r.request.headers)
            raise NotImplementedError('JSON could not be read from server.')

    if prev_thread_name is None or prev_thread_name == '':
        r = requests.get(
            WINDSTORMAPIHOST+"views/thread/{}?size=1&page=1".format(
                action['dependency']
            )
        )
        if r.status_code == 200:
            prev_thread_name = r.json()["results"][0]["name"]

    return action, action_prev

## TODO: This function should be replaced with sysml-windstorm and the data
# from the API.
def template_render(action):
    ## Convert the dictionary
    variables = action['variables'].copy()
    for var in variables:
        variables[var] = variables[var]['value']

    def digitalforge(string):
        # This function is prep for using units
        return action['variables'][string]['value']

    def windstorm(string):
        # This function is prep for using units
        return action['variables'][string]['value']

    print('Replacing variables in files with values.')
    for (dir_path, dir_names, file_names) in os.walk('artifact'):
        for name in file_names:
            thisfile = os.path.join(dir_path, name)
            if 'artifact/.git' in dir_path:
                # Skip the .git folder
                continue

            f = open(thisfile,'r')

            try:
                template = Template(f.read())
            except UnicodeDecodeError:
                print(
                    'Warning: Skipping file {}/{} because it was not text-based.'.format(
                        dir_path, name
                    )
                )
            f.close()

            # Save to temp folder for zip and upload to minio
            with open(os.path.join('tmp',dir_path[8:],name), 'w') as f:
                f.write(template.render(digitalforge=digitalforge,**variables))
            # Overwrite anything in the current folder with the artifact
            with open(os.path.join(VOLUME,dir_path[8:],name), 'w') as f:
                f.write(template.render(digitalforge=digitalforge,**variables))
