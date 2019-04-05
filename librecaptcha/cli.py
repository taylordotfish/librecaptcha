# Copyright (C) 2017, 2019 taylor.fish <contact@taylor.fish>
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

from .errors import UserError
from .frontend import Frontend
from PIL import ImageDraw, ImageFont

from threading import Thread, RLock
from queue import Queue
import io
import json
import os
import subprocess
import sys
import time


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


def draw_lines(image, rows, columns):
    draw = ImageDraw.Draw(image)

    def line(p1, p2):
        draw.line([p1, p2], fill=(255, 255, 255), width=2)

    for i in range(1, rows):
        y = image.height * i // rows - 1
        line((0, y), (image.width, y))

    for i in range(1, columns):
        x = image.width * i // columns - 1
        line((x, 0), (x, image.height))


def draw_indices(image, rows, columns):
    draw = ImageDraw.Draw(image, "RGBA")
    for i in range(rows * columns):
        row = i // columns
        column = i % columns
        corner = (
            image.width * column // columns,
            image.height * (row + 1) // rows,
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


def print_temporary(string, file=sys.stdout):
    end = "" if file.isatty() else "\n"
    print(string, file=file, end=end, flush=True)


def clear_temporary(file=sys.stdout):
    if not file.isatty():
        return
    print("\r\x1b[K", file=file, end="", flush=True)


class CliSolver:
    def __init__(self, solver):
        self.solver = solver
        self.__image_procs = []
        self.__has_display = (os.name == "posix")

    def __run_display(self, img_bytes):
        return subprocess.Popen(
            ["display", "-"], stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

    def __try_display(self, image):
        if not self.__has_display:
            return False
        img_buffer = io.BytesIO()
        image.save(img_buffer, "png")
        img_bytes = img_buffer.getvalue()

        try:
            proc = self.__run_display(img_bytes)
        except FileNotFoundError:
            self.__has_display = False
            return False
        proc.stdin.write(img_bytes)
        proc.stdin.close()
        self.__image_procs.append(proc)
        return True

    def show_image(self, image):
        if not self.__try_display(image):
            image.show()

    def hide_images(self):
        for proc in self.__image_procs:
            proc.terminate()
        self.__image_procs.clear()

    def run(self):
        self.solver.run()


class CliDynamicSolver(CliSolver):
    def __init__(self, solver):
        super().__init__(solver)
        solver.on_initial_image = self.handle_initial_image
        solver.on_tile_image = self.handle_tile_image
        self.image_open = False
        self.image_queue = Queue()
        self.num_pending = 0
        self.lock = RLock()

    def handle_initial_image(self, image, **kwargs):
        solver = self.solver
        num_rows, num_columns = solver.dimensions
        draw_indices(image, num_rows, num_columns)
        self.show_image(image)

        print("Take a look at the grid of tiles that just appeared. ", end="")
        print("({} rows, {} columns)".format(num_rows, num_columns))
        print("Which tiles should be selected?")
        print("(Top-left is 1; bottom-right is {}.)".format(solver.num_tiles))
        indices = read_indices(
            "Enter numbers separated by spaces: ", solver.num_tiles,
        )
        print()
        self.hide_images()
        self.select_initial(indices)
        self.new_tile_loop()
        solver.finish()

    def new_tile_loop(self):
        while self.num_pending > 0:
            print_temporary("Waiting for next image...")
            index, image = self.image_queue.get()
            clear_temporary()
            self.num_pending -= 1
            self.show_image(image)

            print("Take a look at the image that just appeared.")
            accept = input(
                "Should this image be selected? [y/N] ",
            )[:1].lower() == "y"
            print()

            self.hide_images()
            if accept:
                self.select_tile(index)

    # Called from a non-main thread.
    def handle_tile_image(self, index, image, **kwargs):
        self.image_queue.put((index, image))

    def select_initial(self, indices):
        for i, index in enumerate(indices):
            # Avoid sending initial requests simultaneously.
            self.select_tile(index, 0.25 * i)

    def select_tile_sync(self, index):
        self.num_pending += 1
        self.solver.select_tile(index)

    def select_tile(self, index, delay=0):
        def target():
            delay and time.sleep(delay)
            with self.lock:
                self.select_tile_sync(index)
        Thread(target=target, daemon=True).start()


class CliMultiCaptchaSolver(CliSolver):
    def __init__(self, solver):
        super().__init__(solver)
        solver.on_image = self.handle_image

    def handle_image(self, image, **kwargs):
        solver = self.solver
        num_rows, num_columns = solver.dimensions
        draw_lines(image, num_rows, num_columns)
        draw_indices(image, num_rows, num_columns)
        self.show_image(image)

        print("Take a look at the grid of tiles that just appeared. ", end="")
        print("({} rows, {} columns)".format(num_rows, num_columns))
        print("Which tiles should be selected?")
        print("(Top-left is 1; bottom-right is {}.)".format(solver.num_tiles))
        indices = read_indices(
            "Enter numbers separated by spaces: ", solver.num_tiles,
        )
        print()
        self.hide_images()
        solver.select_indices(indices)


BLOCKED_MSG = """\
ERROR: Received challenge type "{}".

This is usually an indication that reCAPTCHA requests from this network are
being blocked.

Try installing Tor (the full installation, not just the browser bundle) and
running this program over Tor with the "torsocks" command.

Alternatively, try waiting a while before requesting another challenge over
this network.
"""


class Cli(Frontend):
    def __init__(self, recaptcha):
        super().__init__(recaptcha)
        rc = recaptcha
        rc.on_goal = self.handle_goal
        rc.on_challenge = self.handle_challenge
        rc.on_challenge_dynamic = self.challenge_dynamic
        rc.on_challenge_multicaptcha = self.challenge_multicaptcha
        rc.on_challenge_blocked = self.challenge_blocked
        rc.on_challenge_unknown = self.challenge_unknown
        self._first = True

    def handle_goal(self, goal, meta, **kwargs):
        if goal:
            print("CHALLENGE OBJECTIVE: {}".format(goal))
            return
        print("WARNING: Could not determine challenge objective.")
        print("Challenge information: {}".format(json.dumps(meta)))

    def handle_challenge(self, ctype, **kwargs):
        if not self._first:
            print("You must solve another challenge.")
            print()
        self._first = False

    def challenge_dynamic(self, solver, **kwargs):
        CliDynamicSolver(solver).run()

    def challenge_multicaptcha(self, solver, **kwargs):
        CliMultiCaptchaSolver(solver).run()

    def challenge_blocked(self, ctype, **kwargs):
        self.raise_challenge_blocked(ctype)

    def challenge_unknown(self, ctype, **kwargs):
        self.raise_challenge_unknown(ctype)

    @classmethod
    def raise_challenge_blocked(cls, ctype):
        print(BLOCKED_MSG.format(ctype), end="")
        raise UserError(
            "Error: Unsupported challenge type: {}.\n".format(ctype) +
            "Requests are most likely being blocked; see the message above.",
        )

    @classmethod
    def raise_challenge_unknown(cls, ctype):
        raise UserError(
            "Error: Got unsupported challenge type: {}\n".format(ctype) +
            "Please file an issue if this problem persists.",
        )
