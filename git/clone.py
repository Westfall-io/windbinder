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
from env import GITHOST, VOLUME

import os

import git

def parse_repopath(repopath, ref):
    rp = repopath.split('/')
    path = {
        'repo': rp[1],
        'org': rp[0],
        'ref': ref
    }
    return path

def clone(action):
    print('Downloading git repo for input artifacts.')
    path = parse_repopath(action['artifact']['full_name'], action['artifact']['ref'])
    #print(path)
    ipath = os.path.join(GITHOST,path['org'], path['repo'])

    # Download the git repo for the artifact
    print('Downloading the repo.')
    repo = git.Repo.clone_from(ipath, 'artifact')
    repo.git.checkout(path['ref'])
    return repo

def init():
    print('Initializing git repo.')
    # Git init the directory
    repo2 = git.Repo.init(VOLUME)
    repo2.git.add(all=True)
    # Commit everything here
    repo2.index.commit(":robot: Setting base files.")
    return repo2
