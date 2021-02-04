# Copyright (C) 2017, 2019, 2021 taylor.fish <contact@taylor.fish>
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
# along with librecaptcha.  If not, see <http://www.gnu.org/licenses/>.

from slimit.parser import Parser
from slimit import ast
import requests

import json
import os
import os.path
import re
import sys

SHOW_WARNINGS = False


def make_parser_raw():
    return Parser()


def make_parser_silent():
    # File descriptor hackiness to silence warnings
    null_fd = os.open(os.devnull, os.O_RDWR)
    old_fd = os.dup(2)
    try:
        os.dup2(null_fd, 2)
        return make_parser_raw()
    finally:
        os.dup2(old_fd, 2)
        os.close(null_fd)
        os.close(old_fd)


make_parser = make_parser_silent
if SHOW_WARNINGS:
    make_parser = make_parser_raw


def load_javascript(url, user_agent):
    print("Downloading <{}>...".format(url), file=sys.stderr)
    r = requests.get(url, headers={
        "User-Agent": user_agent,
    })
    return r.text


def extract_strings(javascript):
    print("Extracting strings...", file=sys.stderr)
    # Hack to work around https://github.com/rspivak/slimit/issues/52
    KEYWORDS = r"(?:catch|delete|return|throw)"
    javascript = re.sub(rf"(\.\s*{KEYWORDS})\b", r"\1_", javascript)
    javascript = re.sub(rf"\b({KEYWORDS})(\s*:)", r"'\1'\2", javascript)
    parsed = make_parser().parse(javascript)
    strings = []

    def add_strings(tree, strings):
        if tree is None:
            return

        if not isinstance(tree, (ast.Node, list, tuple)):
            raise TypeError("Unexpected item: {!r}".format(tree))

        if isinstance(tree, ast.String):
            strings.append(tree.value[1:-1])

        children = tree
        if isinstance(tree, ast.Node):
            children = tree.children()

        for child in children:
            add_strings(child, strings)

    add_strings(parsed, strings)
    return strings


def extract_and_save(url, path, version, rc_version, user_agent):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        print("{}/{}".format(version, rc_version), file=f)
        js = load_javascript(url, user_agent)
        strings = extract_strings(js)
        strings_json = json.dumps(strings)
        print('Saving strings to "{}"...'.format(path), file=sys.stderr)
        f.write(strings_json)
        return strings
