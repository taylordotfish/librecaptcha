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

from .librecaptcha import get_token, __version__
import sys


def usage(exit=True):
    print("Usage:", file=sys.stderr)
    print("  librecaptcha.py [--debug] <api-key> <site-url>", file=sys.stderr)
    print("  librecaptcha.py -h | --help | --version\n", file=sys.stderr)
    print("<api-key> is the reCAPTCHA API key to use.\n", file=sys.stderr)
    print("<site-url> is the base URL of the site that contains the reCAPTCHA "
          "challenge.", file=sys.stderr)
    print("It should start with http:// or https:// and include the hostname, "
          "but nothing else.", file=sys.stderr)
    print("For example: https://example.com", file=sys.stderr)
    if exit:
        sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == "--version":
        print(__version__)
        return

    debug = True
    try:
        args.pop(args.index("--debug"))
    except ValueError:
        debug = False

    try:
        api_key, site_url = args
    except ValueError:
        usage()

    uvtoken = get_token(api_key, site_url, debug=debug)
    print("Received token. This token should usually be submitted with the "
          'form as the value of the "g-recaptcha-response" field.')
    print("Token: {}".format(uvtoken))


if __name__ == "__main__":
    main()
