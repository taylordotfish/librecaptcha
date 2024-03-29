#!/usr/bin/env python3
# Copyright (C) 2019, 2021 taylor.fish <contact@taylor.fish>
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

import requests
from html.parser import HTMLParser
import json
import os.path
import re
import sys

USAGE = """\
Usage:
  update-user-agents.py
  update-user-agents.py <html-file>
  update-user-agents.py -h | --help
"""

URL = "https://techblog.willshouse.com/2012/01/03/most-common-user-agents/"
SCRIPT_DIR = os.path.dirname(__file__)
OUT_PATH = os.path.join(SCRIPT_DIR, "..", "librecaptcha", "user_agent_data.py")
NUM_ENTRIES = 30

HEADER = """\
# This file was automatically generated by update_user_agents.py using data
# from <https://techblog.willshouse.com/2012/01/03/most-common-user-agents/>.

# flake8: noqa
USER_AGENTS = \
"""

FOOTER = "\n"


class Parser(HTMLParser):
    def __init__(self):
        self.desc_seen = False
        self.result = None
        super().__init__()

    def handle_data(self, data):
        if self.result is not None:
            return
        if data is None:
            return
        if not self.desc_seen:
            self.desc_seen = bool(re.search(r"\bplain-text\b", data))
            return
        if re.match(r"\s*Mozilla/", data):
            self.result = data


def get_agents(data):
    agents = []
    for agent in data.strip().splitlines()[:NUM_ENTRIES]:
        if len(agents) >= NUM_ENTRIES:
            break
        if re.match(r"\b(iPhone|iPad|Android)\b", agent):
            continue
        agents.append(agent)
    return agents


def write_agents(agents, file):
    print(HEADER, file=file, end="")
    json.dump(agents, file, indent=4)
    print(FOOTER, file=file, end="")


def main():
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        print(USAGE, end="")
        sys.exit(0)

    if len(sys.argv) > 2:
        print(USAGE, end="", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf8") as f:
            text = f.read()
    else:
        text = requests.get(URL).text

    parser = Parser()
    parser.feed(text)
    with open(OUT_PATH, "w", encoding="utf8") as f:
        agents = get_agents(parser.result)
        write_agents(agents, f)


if __name__ == "__main__":
    main()
