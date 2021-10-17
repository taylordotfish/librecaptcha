#!/usr/bin/env python3
# Copyright (C) 2016-2019 taylor.fish <contact@taylor.fish>
#
# This file is part of librecaptcha.
#
# librecaptcha is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# librecaptcha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with librecaptcha.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_URL = "https://github.com/taylordotfish/librecaptcha"
DESC_REPLACEMENTS = {
    ".. _LICENSE: LICENSE":
    ".. _LICENSE: {}/blob/master/LICENSE".format(REPO_URL),
}


def long_description():
    with open(os.path.join(SCRIPT_DIR, "README.rst"), encoding='utf-8') as f:
        lines = f.read().splitlines()
    result = []
    iterator = iter(lines)
    for line in iterator:
        if line.startswith(".. image::"):
            while "Screenshot attribution" not in next(iterator):
                pass
            next(iterator)
        else:
            result.append(DESC_REPLACEMENTS.get(line, line) + "\n")
    return "".join(result)


setup(
    long_description=long_description(),
)
