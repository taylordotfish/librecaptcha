#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
import os
import os.path

PORT = 55476

RC_JS = """\
"/m/test1";
"Select all squares with <strong>Test 1</strong>";
"/m/test2";
"Select all squares with <strong>Test 2</strong>";
"/m/test3";
"Select all squares with <strong>Test 3</strong>";
"/m/test4";
"Select all squares with <strong>Test 4</strong>";
"/m/test5";
"Select all squares with <strong>Test 5</strong>";
"/m/test6";
"Select all squares with <strong>Test 6</strong>";
"/m/test7";
"Select all squares with <strong>Test 7</strong>";
"/m/test8";
"Select all squares with <strong>Test 8</strong>";
"""

ANCHOR = """\
<input id="recaptcha-token" value="initial-token" />
"""

INITIAL_RRESP = """)]}'
[
    "rresp",
    "test-token-1",
    null,
    1234,
    [
        "pmeta",
        [
            "/m/test1",
            null,
            1234,
            3,
            3,
            null,
            "test 1",
            []
        ],
        null,
        [1, 2, 3, 4]
    ],
    "dynamic",
    null,
    ["abcd", "abcd"],
    "abcd",
    "test-p-1",
    null,
    null,
    "abcd"
]
"""

UVRESPS = [
    """)]}'
    [
        "uvresp",
        "abcd",
        1234,
        null,
        null,
        null,
        null,
        [
            "rresp",
            "test-token-2",
            null,
            1234,
            [
                "pmeta",
                null,
                null,
                null,
                null,
                [
                    [
                        [
                            "/m/test2",
                            null,
                            1234,
                            4,
                            4,
                            null,
                            null,
                            []
                        ],
                        [
                            "/m/test3",
                            null,
                            1234,
                            4,
                            4,
                            null,
                            null,
                            []
                        ],
                        [
                            "/m/test4",
                            null,
                            1234,
                            4,
                            4,
                            null,
                            null,
                            []
                        ]
                    ],
                    []
                ]
            ],
            "multicaptcha",
            null,
            ["abcd", "abcd"],
            null,
            "test-p-2",
            null,
            null,
            "abcd"
        ]
    ]
    """,
    """)]}'
    [
        "uvresp",
        "final-token",
        1234,
        1234,
        null,
        null,
        null,
        null,
        null,
        "abcd"
    ]
    """,
]

DRESP_TEMPLATE = """)]}}'
[
    "dresp",
    "{token}",
    ["{id}"],
    null,
    [],
    "{p}"
]
"""


class State:
    def __init__(self):
        self.reset()

    def reset(self):
        self.uvresp_index = -1
        self.dresp_num = 0
        self.next_image = None

    @property
    def challenge_type(self) -> Optional[str]:
        if self.uvresp_index in [-1]:
            return "dynamic"
        if self.uvresp_index in [0]:
            return "multicaptcha"
        return None

    def reload(self) -> str:
        self.reset()
        self.next_image = self._initial_image
        return INITIAL_RRESP

    def replaceimage(self) -> str:
        self.dresp_num += 1
        challenge_type = self.challenge_type
        if challenge_type == "multicaptcha":
            self.next_image = f"multi{STATE.dresp_num + 1}"
        elif challenge_type == "dynamic":
            self.next_image = f"tile{1 + (STATE.dresp_num - 1) % 16}"
        else:
            raise RuntimeError(f"Invalid challenge type: {challenge_type}")

        return DRESP_TEMPLATE.format(
            token=f"dresp-token-{STATE.dresp_num}",
            id=STATE.next_image,
            p=f"dresp-p-{STATE.dresp_num}",
        )

    def payload_path(self) -> Optional[str]:
        if self.next_image is None:
            return None
        path = os.path.join("images", "jpeg", f"{self.next_image}.jpg")
        self.next_image = None
        return path

    def userverify(self) -> str:
        self.uvresp_index += 1
        self.dresp_num = 0
        self.next_image = self._initial_image
        return UVRESPS[self.uvresp_index]

    @property
    def _initial_image(self) -> Optional[str]:
        return {
            None: None,
            "dynamic": "dynamic",
            "multicaptcha": "multi1",
        }[self.challenge_type]


STATE = State()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/api.js"):
            self.handle_api_js()
        elif self.path.endswith("/recaptcha__en.js"):
            self.handle_rc_js()
        elif "/anchor?" in self.path:
            self.handle_anchor()
        elif "/payload?" in self.path:
            self.handle_payload()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_api_js(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"/recaptcha/releases/test-version/\n")

    def handle_rc_js(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(RC_JS.encode())

    def handle_anchor(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(ANCHOR.encode())

    def handle_payload(self):
        path = STATE.payload_path()
        if path is None:
            self.send_response(400)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.end_headers()
        with open(path, "rb") as f:
            self.wfile.write(f.read())

    def do_POST(self):
        content_type = self.headers.get("Content-Type")
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)

        print()
        print(f"  POST data ({content_type}):")
        print(f"  {repr(data)}")

        if "/reload?" in self.path:
            self.handle_reload()
        elif "/replaceimage?" in self.path:
            self.handle_replaceimage()
        elif "/userverify?" in self.path:
            self.handle_userverify()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_reload(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(STATE.reload().encode())

    def handle_replaceimage(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(STATE.replaceimage().encode())

    def handle_userverify(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(STATE.userverify().encode())


def main():
    os.chdir(os.path.dirname(__file__) or ".")
    server = HTTPServer(("", PORT), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
