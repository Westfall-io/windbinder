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
from env import *

import git

def print_files_from_git(root, level=0):
    for entry in root:
        print(f'{"-" * 4 * level}| {entry.path}, {entry.type}')
        if entry.type == "tree":
            print_files_from_git(entry, level + 1)

def add_repo_and_print():
    repo2 = git.Repo(VOLUME)
    t = repo2.head.commit.tree
    print_files_from_git(t)
    return repo2

def git_add(repo2):
    repo2.git.add(all=True)
    return

def git_configure():
    print('Printing all files in commit.')
    repo2 = add_repo_and_print()

    print('Adding all new files since last commit.')
    git_add(repo2)

    print('Finding all changed files.')
    files = [item.a_path for item in repo2.index.diff('HEAD')]
    return files
