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

import os

from junitparser import JUnitXml, Error, Failure

class JUnitErrorException(Exception):
    pass

def check_is_junit(file):
    # Check if this file is a junit.xml

    # Get the extension
    _, ext = os.path.splitext(file)
    if '.xml' == ext:
        # This might be a junit test
        print('Checking if this file ({}) is a junit report.'.format(file))

        try:
            # Try to read it as junit
            xml = JUnitXml.fromfile(os.path.join(VOLUME, file))
        except Exception as e:
            # This couldn't be parsed.
            print("File {} wasn't a readable junit report.".format(file))
            xml = ''
        return xml != '', xml
    else:
        # This didn't have the correct file type for junit
        print('File type: {} found in file {}.'.format(ext, file))
        return False, ''


def handle_junit_case(case):
    # Handle case
    r = case.result
    if len(r) == 0:
        return

    if r[0].__class__==Error or r[0].__class__==Failure:
        raise JUnitErrorException

def handle_junit_suite(suite):
    # handle suites
    for case in suite:
        handle_junit_case(case)

def find_junit_errors(xml):
    try:
        for suite in xml:
            handle_junit_suite(suite)

    except JUnitErrorException:
        print('Error Found')
        return True

    print('Successful test found.')
    return False

def find_junit(file):
    check, xml = check_is_junit(file)
    if not check:
        return None

    error = find_junit_errors(file)
    return error

def copy_file(file):
    try:
        shutil.copyfile(
            os.path.join(VOLUME, file),
            os.path.join('/tmp/digitalforge', file)
        )
        return None
    except:
        # If we run into a file that we can't copy, just forget it ever existed.
        return None

def check_files(files):
    error = None # All junit files didn't return an error
    for file in files:
        if error is None:
            error = find_junit(file)
        else:
            if not error: # Haven't already found an error
                error = find_junit(file)

        copy_file(file)

    return error
