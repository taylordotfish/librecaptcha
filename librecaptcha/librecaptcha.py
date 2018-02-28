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

from .user_agents import random_user_agent
from .extract_strings import extract_and_save

from PIL import Image, ImageDraw, ImageFont
import requests

from html.parser import HTMLParser
from urllib.parse import urlparse
import base64
import io
import json
import os
import os.path
import re
import subprocess
import sys
import time

__version__ = "0.4.0"

BASE_URL = "https://www.google.com/recaptcha/api2/"
API_JS_URL = "https://www.google.com/recaptcha/api.js"
JS_URL_TEMPLATE = "https://www.gstatic.com/recaptcha/api2/{}/recaptcha__en.js"

STRINGS_VERSION = "0.1.0"
STRINGS_PATH = os.path.join(
    os.path.expanduser("~"), ".cache", "librecaptcha", "cached-strings",
)

DYNAMIC_SELECT_DELAY = 5
FIND_GOAL_SEARCH_DISTANCE = 10


def get_font(size):
    typefaces = [
        "FreeSans", "LiberationSans-Regular", "DejaVuSans", "Arial", "arial",
    ]

    for typeface in typefaces:
        try:
            return ImageFont.truetype(typeface, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


FONT_SIZE = 16
FONT = get_font(FONT_SIZE)


def get_full_url(url):
    return BASE_URL.rstrip("/") + "/" + url.lstrip("/")


def get_rc_site_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        raise ValueError("URL has no scheme.")
    if parsed.scheme not in ["http", "https"]:
        raise ValueError("Invalid scheme: {}".format(parsed.scheme))
    if not parsed.hostname:
        raise ValueError("URL has no hostname.")
    port = parsed.port
    if port is None:
        port = {"http": 80, "https": 443}[parsed.scheme]
    return "{}://{}:{}".format(parsed.scheme, parsed.hostname, port)


def rc_base64(string):
    data = string
    if isinstance(string, str):
        data = string.encode()
    return base64.b64encode(data, b"-_").decode().replace("=", ".")


def load_rc_json(text):
    return json.loads(text.split("\n", 1)[1])


def get_meta(pmeta, probable_index):
    if not isinstance(pmeta, list):
        raise TypeError("pmeta is not a list: {!r}".format(pmeta))

    def matches(meta):
        if meta and isinstance(meta, list):
            return True

    if probable_index < len(pmeta):
        meta = pmeta[probable_index]
        if matches(meta):
            return meta

    for child in pmeta:
        if matches(child):
            return child
    raise RuntimeError("Could not find meta; pmeta: {!r}".format(pmeta))


def get_rresp(uvresp):
    if not isinstance(uvresp, list):
        raise TypeError("uvresp is not a list: {!r}".format(uvresp))

    for child in uvresp:
        if child and isinstance(child, list) and child[0] == "rresp":
            return child
    return None


def read_indices(prompt, max_index):
    while True:
        print(prompt, end="", flush=True)
        line = input()
        try:
            indices = [int(i) - 1 for i in line.split()]
        except ValueError:
            print("Invalid input.")
            continue
        if all(0 <= i < max_index for i in indices):
            return indices
        print("Numbers out of bounds.")


def get_js_strings(user_agent, rc_version):
    def get_json():
        with open(STRINGS_PATH) as f:
            version, text = f.read().split("\n", 1)
            if version != "{}/{}".format(STRINGS_VERSION, rc_version):
                raise OSError("Incorrect version: {}".format(version))
            return json.loads(text)

    try:
        return get_json()
    except (OSError, ValueError, json.JSONDecodeError):
        pass

    result = extract_and_save(
        JS_URL_TEMPLATE.format(rc_version), STRINGS_PATH, STRINGS_VERSION,
        rc_version, user_agent,
    )

    print()
    return result


def get_rc_version(user_agent):
    match = re.search(r"/recaptcha/api2/(.+?)/", requests.get(
        API_JS_URL, headers={
            "User-Agent": user_agent,
        }
    ).text)
    if match is None:
        raise RuntimeError("Could not extract version from api.js.")
    return match.group(1)


def get_image(data):
    return Image.open(io.BytesIO(data))


def draw_lines(image, rows, columns):
    draw = ImageDraw.Draw(image)
    for i in range(1, rows):
        y = int(image.height * i / rows) - 1
        draw.line([(0, y), (image.width, y)], fill=(255, 255, 255), width=2)

    for i in range(1, columns):
        x = int(image.width * i / columns) - 1
        draw.line([(x, 0), (x, image.height)], fill=(255, 255, 255), width=2)


def draw_indices(image, rows, columns):
    draw = ImageDraw.Draw(image, "RGBA")
    for i in range(rows * columns):
        row = i // columns
        column = i % columns
        corner = (
            int(image.width * column / columns),
            int(image.height * (row + 1) / rows),
        )
        text_loc = (
            corner[0] + round(FONT_SIZE / 2),
            corner[1] - round(FONT_SIZE * 1.5),
        )

        text = str(i + 1)
        text_size = FONT.getsize(text)

        draw.rectangle([
            (text_loc[0] - round(FONT_SIZE / 10), text_loc[1]), (
                text_loc[0] + text_size[0] + round(FONT_SIZE / 10),
                text_loc[1] + text_size[1] + round(FONT_SIZE / 10),
            ),
        ], fill=(0, 0, 0, 128))

        draw.text(text_loc, str(i + 1), fill=(255, 255, 255), font=FONT)


class Solver:
    def __init__(self, recaptcha):
        self.rc = recaptcha
        self._image_procs = []

    def show_image(self, image):
        if not os.path.isfile("/usr/bin/env"):
            image.show()
            return

        img_buffer = io.BytesIO()
        image.save(img_buffer, "png")
        img_bytes = img_buffer.getvalue()

        proc = subprocess.Popen(
            ["/usr/bin/env", "display", "-"], stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc.stdin.write(img_bytes)
        proc.stdin.close()
        self._image_procs.append(proc)

    def hide_images(self):
        for proc in self._image_procs:
            proc.terminate()
        self._image_procs.clear()


class DynamicSolver(Solver):
    def __init__(self, recaptcha, pmeta):
        super().__init__(recaptcha)
        self.original_selections = []
        self.selections = []

        meta = get_meta(pmeta, 1)
        self.num_rows = meta[3]
        self.num_columns = meta[4]
        self.num_tiles = self.num_rows * self.num_columns
        self.current_index = self.num_tiles - 1
        self.rc.print_challenge_goal(meta)

    def run(self):
        self.first_payload()
        for index in self.original_selections:
            self.select_tile(index)
        return self.selections

    def first_payload(self):
        image = get_image(self.rc.get("payload", api=False, params={
            "c": self.rc.current_token,
            "k": self.rc.api_key,
        }).content)
        draw_indices(image, self.num_rows, self.num_columns)
        self.show_image(image)

        print("Take a look at the grid of tiles that just appeared. ", end="")
        print("({} rows, {} columns)".format(self.num_rows, self.num_columns))
        print("Which tiles should be selected?")
        print("(Top-left tile is 1; bottom-right tile is {}.)".format(
            self.num_tiles,
        ))

        indices = read_indices(
            "Enter numbers separated by spaces: ", self.num_tiles,
        )
        self.hide_images()
        self.original_selections += indices
        print()

    def select_tile(self, index):
        selected = True
        current_index = index
        while selected:
            last_request_time = time.monotonic()
            selected = self.tile_iteration(current_index)
            time_elapsed = time.monotonic() - last_request_time
            sleep_duration = max(DYNAMIC_SELECT_DELAY - time_elapsed, 0)

            if sleep_duration >= 0.25:
                print("Waiting (to avoid sending requests too quickly)...")
            print()
            time.sleep(sleep_duration)
            current_index = self.current_index

    def tile_iteration(self, index):
        self.selections.append(index)
        r = self.rc.post("replaceimage", data={
            "c": self.rc.current_token,
            "ds": "[{}]".format(index),
        })

        data = load_rc_json(r.text)
        self.current_index += 1

        self.rc.current_token = data[1]
        replacement_id = data[2][0]

        image = get_image(self.rc.get("payload", api=False, params={
            "c": self.rc.current_token,
            "k": self.rc.api_key,
            "id": replacement_id,
        }).content)
        self.show_image(image)

        print("Take a look at the image that just appeared.")
        selected = input(
            "Should this image be selected? [y/N] ",
        )[:1].lower() == "y"
        self.hide_images()
        return selected


class MultiCaptchaSolver(Solver):
    def __init__(self, recaptcha, pmeta):
        super().__init__(recaptcha)
        self.selection_groups = []

        self.num_rows = None
        self.num_columns = None
        self.challenge_type = None
        self.num_tiles = None

        self.previous_token = None
        self.previous_id = None
        self.id = "2"

        self.metas = list(get_meta(pmeta, 5)[0])
        self.next_challenge()

    def run(self):
        self.first_payload()
        while self.metas:
            self.replace_image()
        return self.selection_groups

    def next_challenge(self):
        meta = self.metas.pop(0)
        self.num_rows = meta[3]
        self.num_columns = meta[4]
        self.num_tiles = self.num_rows * self.num_columns
        self.rc.print_challenge_goal(meta)

    def get_answer(self):
        print("Take a look at the grid of tiles that just appeared. ", end="")
        print("({} rows, {} columns)".format(self.num_rows, self.num_columns))
        print("Which tiles should be selected?")
        print("(Top-left tile is 1; bottom-right tile is {}.)".format(
            self.num_tiles,
        ))

        indices = read_indices(
            "Enter numbers separated by spaces: ", self.num_tiles,
        )
        self.hide_images()
        self.selection_groups.append(list(sorted(indices)))
        print()

    def show_image(self, image):
        draw_lines(image, self.num_rows, self.num_columns)
        draw_indices(image, self.num_rows, self.num_columns)
        super().show_image(image)

    def first_payload(self):
        image = get_image(self.rc.get("payload", api=False, params={
            "c": self.rc.current_token,
            "k": self.rc.api_key,
        }).content)
        self.show_image(image)
        self.get_answer()

    def replace_image(self):
        selections = self.selection_groups[-1]
        r = self.rc.post("replaceimage", data={
            "c": self.rc.current_token,
            "ds": json.dumps([selections], separators=",:"),
        })

        data = load_rc_json(r.text)
        self.previous_token = self.rc.current_token
        self.rc.current_token = data[1]

        replacement_id = (data[2] or [None])[0]
        self.previous_id = self.id
        self.id = replacement_id
        self.next_challenge()

        image = get_image(self.rc.get("payload", api=False, params={
            "c": self.previous_token,
            "k": self.rc.api_key,
            "id": self.previous_id,
        }).content)
        self.show_image(image)
        self.get_answer()


class ReCaptcha:
    def __init__(self, api_key, site_url, debug, user_agent=None,
                 make_requests=True):
        self.api_key = api_key
        self.site_url = get_rc_site_url(site_url)
        self._debug = debug
        self.co = rc_base64(self.site_url)

        self.first_token = None
        self.current_token = None
        self.user_agent = user_agent or random_user_agent()

        self.js_strings = None
        self.rc_version = None
        if make_requests:
            self.rc_version = get_rc_version(self.user_agent)
            self.js_strings = get_js_strings(self.user_agent, self.rc_version)

    def debug(self, *args, **kwargs):
        if self._debug:
            print(*args, file=sys.stderr, **kwargs)

    def find_challenge_goal(self, id):
        start = 0
        matching_strings = []
        try:
            while True:
                index = self.js_strings.index(id, start)
                for i in range(FIND_GOAL_SEARCH_DISTANCE):
                    next_str = self.js_strings[index + i + 1]
                    if next_str.startswith("Select all "):
                        matching_strings.append((i, index, next_str))
                start = index + FIND_GOAL_SEARCH_DISTANCE + 1
        except (ValueError, IndexError):
            pass

        try:
            goal = min(matching_strings)[2]
        except ValueError:
            return None
        return goal.replace("<strong>", "").replace("</strong>", "")

    def print_challenge_goal(self, meta):
        print("Challenge information: {}".format(json.dumps(meta)))
        goal = self.find_challenge_goal(meta[0])
        print(
            "Could not determine challenge objective. See the challenge "
            "information above for more information."
            if goal is None else "CHALLENGE OBJECTIVE: {}".format(goal)
        )

    def get_headers(self, headers):
        headers = headers or {}
        if "User-Agent" not in headers:
            headers["User-Agent"] = self.user_agent
        return headers

    def get(self, url, *, params=None, api=True, headers=None,
            allow_errors=None, **kwargs):
        params = params or {}
        if api:
            params["k"] = self.api_key
            params["v"] = self.rc_version
        headers = self.get_headers(headers)

        r = requests.get(
            get_full_url(url), params=params, headers=headers, **kwargs,
        )

        self.debug("[http] [get] {}".format(r.url))
        if not (allow_errors is True or r.status_code in (allow_errors or {})):
            r.raise_for_status()
        return r

    def post(self, url, *, params=None, data=None, api=True, headers=None,
             allow_errors=None, no_debug_response=False, **kwargs):
        params = params or {}
        data = data or {}
        if api:
            params["k"] = self.api_key
            data["v"] = self.rc_version
        headers = self.get_headers(headers)

        r = requests.post(
            get_full_url(url), params=params, data=data, headers=headers,
            **kwargs,
        )

        self.debug("[http] [post] {}".format(r.url))
        self.debug("[http] [post] [data] {!r}".format(data))
        if not no_debug_response:
            self.debug("[http] [post] [response] {}".format(r.text))
        if not (allow_errors is True or r.status_code in (allow_errors or {})):
            r.raise_for_status()
        return r

    def request_first_token(self):
        class Parser(HTMLParser):
            def __init__(p_self):
                p_self.token = None
                super().__init__()

            def handle_starttag(p_self, tag, attrs):
                attrs = dict(attrs)
                if attrs.get("id") == "recaptcha-token":
                    p_self.token = attrs.get("value")

        text = self.get("anchor", params={"co": self.co}).text
        parser = Parser()
        parser.feed(text)

        if not parser.token:
            raise RuntimeError(
                "Could not get first token. Response:\n{}".format(text),
            )

        self.first_token = parser.token
        self.current_token = self.first_token

    def verify(self, response):
        response_text = json.dumps({"response": response}, separators=",:")
        response_b64 = rc_base64(response_text)

        self.debug("Sending verify request...")
        r = self.post("userverify", data={
            "c": self.current_token,
            "response": response_b64,
        })

        uvresp = load_rc_json(r.text)
        self.debug("Got verify response: {!r}".format(uvresp))

        rresp = get_rresp(uvresp)
        uvresp_token = uvresp[1]
        return (uvresp_token, rresp)

    def solve_all(self):
        self.request_first_token()
        rresp = self.get_first_rresp()
        while rresp is not None:
            uv_token, rresp = self.solve_challenge(rresp)
            if rresp is not None:
                print("You must solve another challenge.")
                print()
        return uv_token

    def get_first_rresp(self):
        self.debug("Getting first rresp...")
        r = self.post("reload", data={"reason": "fi", "c": self.first_token})
        rresp = load_rc_json(r.text)
        self.debug("Got first rresp: {!r}".format(rresp))
        return rresp

    def solve_challenge(self, rresp):
        challenge_type = rresp[5]
        self.debug("Challenge type: {}".format(challenge_type))

        if challenge_type == "default":
            print('ERROR: Received challenge type "default".')
            print("This is usually an indication that reCAPTCHA requests from "
                  "this network are being blocked.")
            print("Try installing Tor (the full installation, not just the "
                  "browser bundle) and running this program over Tor with the "
                  '"torsocks" command.')
            print("Alternatively, try waiting a while before requesting "
                  "another challenge over this network.")
            print()
            raise RuntimeError(
                "Unsupported challenge type. Requests are most likely being "
                "blocked; see the message above.",
            )

        if challenge_type not in ["dynamic", "multicaptcha"]:
            raise RuntimeError(
                "Unsupported challenge type: {}".format(challenge_type),
            )

        pmeta = rresp[4]
        self.debug("pmeta: {}".format(pmeta))

        self.current_token = rresp[1]
        self.debug("Current token: {}".format(self.current_token))

        solver_class = {
            "dynamic": DynamicSolver,
            "multicaptcha": MultiCaptchaSolver,
        }[challenge_type]

        solver = solver_class(self, pmeta)
        response = solver.run()
        return self.verify(response)


def get_token(api_key, site_url, debug=False, user_agent=None):
    r = ReCaptcha(api_key, site_url, debug=debug, user_agent=None)
    uvtoken = r.solve_all()
    return uvtoken
