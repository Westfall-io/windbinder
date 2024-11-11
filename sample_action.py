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
SAMPLE_ACTION = {
    "id": 18,
    "declaredName": "collectData",
    "qualifiedName": "Requirements::Valid_Test::collectData",
    "artifact": {
        "id": 3,
        "full_name": "Westfall/fortran_greaterthan",
        "commit_url": "http://artifacts.westfall.io/Westfall/fortran_greaterthan/commit/fa8f69f17ab910a9126d9338f19dc23062887c04",
        "ref": "main",
        "commit": "84455bbbb558579acc17427adf06af4530ba4abb",
        "date": "2023-10-17T17:41:36.606126"
    },
    "container": {
        "id": 4,
        "resource_url": "core.harbor.domain/fortran-containers/fortran-greaterthan:0.1.0",
        "project": "fortran-containers",
        "image": "fortran-greaterthan",
        "tag": "0.1.0",
        "digest": "a5ad39fb0bf5ea8168938c2f21cfcfb2c1addad8ad98b949a1b8a6edc5c76780",
        "date": "2023-10-17T21:29:44.567434"
    },
    "variables": {
        "var1": {
          "value": 10,
          "units": "u.one"
        },
        "var2": {
          "value": 3,
          "units": "u.one"
        }
    },
    'dependency': None
}
