# Copyright (C) 2017 nickolas360 <contact@nickolas360.com>
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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4"
    " (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",

    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",

    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101"
    " Firefox/54.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.86 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101"
    " Firefox/54.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/59.0.3071.86 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.86 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30"
    " (KHTML, like Gecko) Version/10.1 Safari/603.1.30",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.104 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.2.5"
    " (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.109 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.115 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101"
    " Firefox/54.0",

    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101"
    " Firefox/54.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",

    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.888",

    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",

    "Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4"
    " (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.2.5"
    " (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5",

    "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",

    "Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101"
    " Firefox/54.0",

    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101"
    " Firefox/52.0",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.104 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.109 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.115 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/59.0.3071.104 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/56.0.2924.87 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/59.0.3071.109 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/56.0.2924.87 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8"
    " (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML,"
    " like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101"
    " Firefox/54.0",

    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"
    " Trident/5.0)",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/58.0.3029.81 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.898",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101"
    " Firefox/54.0",

    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101"
    " Firefox/40.1",

    "Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101"
    " Firefox/45.0",

    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",

    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/51.0.2704.106 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/55.0.2883.87 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:53.0) Gecko/20100101"
    " Firefox/53.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/57.0.2987.133 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/57.0.2987.133 Safari/537.36",

    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;"
    " Trident/5.0)",

    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/59.0.3071.86 Safari/537.36",
]


def random_user_agent():
    return random.choice(USER_AGENTS)
