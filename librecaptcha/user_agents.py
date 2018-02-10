# Copyright (C) 2017-2018 nickolas360 <contact@nickolas360.com>
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

import random

# From <https://techblog.willshouse.com/2012/01/03/most-common-user-agents/>
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 "
    "Firefox/57.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 "
    "(KHTML, like Gecko) Version/11.0.2 Safari/604.4.7",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 "
    "Firefox/58.0",

    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/64.0.3282.140 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 "
    "(KHTML, like Gecko) Version/11.0.3 Safari/604.5.6",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",

    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 "
    "Firefox/57.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 "
    "Firefox/57.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/63.0.3239.84 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 "
    "Firefox/58.0",

    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",

    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 "
    "Firefox/58.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/64.0.3282.119 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 "
    "Firefox/57.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/63.0.3239.132 Safari/537.36 OPR/50.0.2762.67",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 "
    "Firefox/52.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 "
    "Firefox/58.0",

    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",

    "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",

    "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.4.7 "
    "(KHTML, like Gecko) Version/11.0.2 Safari/604.4.7",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/64.0.3282.140 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/63.0.3239.132 Safari/537.36 OPR/50.0.2762.58",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 "
    "Firefox/57.0",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/63.0.3239.84 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/64.0.3282.119 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",

    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/64.0.3282.119 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:57.0) Gecko/20100101 "
    "Firefox/57.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 "
    "(KHTML, like Gecko) Version/11.0.3 Safari/604.5.6",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 "
    "(KHTML, like Gecko) Version/11.0.1 Safari/604.3.5",

    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/51.0.2704.106 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/63.0.3239.108 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/64.0.3282.140 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; rv:57.0) Gecko/20100101 Firefox/57.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/63.0.3239.132 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:57.0) Gecko/20100101 "
    "Firefox/57.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.4.7 "
    "(KHTML, like Gecko) Version/11.0.2 Safari/604.4.7",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 "
    "Firefox/52.0",

    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; "
    "Trident/5.0)",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 "
    "Firefox/59.0",

    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; "
    "Trident/5.0)",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 "
    "Firefox/58.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.5.6 "
    "(KHTML, like Gecko) Version/11.0.3 Safari/604.5.6",

    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 "
    "Firefox/56.0",

    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 "
    "Firefox/57.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/62.0.3202.94 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/63.0.3239.84 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:58.0) Gecko/20100101 "
    "Firefox/58.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/63.0.3239.108 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:58.0) Gecko/20100101 "
    "Firefox/58.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.64",

    "Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 "
    "(KHTML, like Gecko) Version/11.0 Mobile/15C202 Safari/604.1",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 "
    "(KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 "
    "(KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",

    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 "
    "Firefox/52.0",

    "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0",
]


def random_user_agent():
    return random.choice(USER_AGENTS)
