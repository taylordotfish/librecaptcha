# Copyright (C) 2019 cyclopsian (https://github.com/cyclopsian)
# Copyright (C) 2019 taylor.fish <contact@taylor.fish>
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

from .cli import Cli
from .errors import UserExit, GtkImportError
from .frontend import Frontend

from threading import Thread, RLock
import html
import json
import math
import re

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
except ImportError as e:
    raise GtkImportError from e

# Disable GTK warnings
GLib.log_set_writer_func(lambda *args: GLib.LogWriterOutput.HANDLED)


def image_to_gdk_pixbuf(image):
    width, height = image.size
    image_bytes = GLib.Bytes.new(image.tobytes())
    has_alpha = image.mode == "RGBA"
    bpp = 4 if has_alpha else 3
    return GdkPixbuf.Pixbuf.new_from_bytes(
        image_bytes, GdkPixbuf.Colorspace.RGB,
        has_alpha, 8, width, height, width * bpp,
    )


class ChallengeDialogWidget(Gtk.Dialog):
    css_provider = None

    def __init__(self):
        super().__init__()
        self.columns = 0
        self.grid = Gtk.Grid.new()
        self.set_title("CAPTCHA Challenge")
        self.set_icon_name("view-refresh-symbolic")

        self.verify = self.add_button("", Gtk.ResponseType.OK)
        context = self.verify.get_style_context()
        context.add_class("suggested-action")
        self.set_resizable(False)

        self.content = content = self.get_content_area()
        content.set_spacing(6)
        for dir in ["top", "right", "bottom", "left"]:
            getattr(content, "set_margin_" + dir)(6)

        self.header = Gtk.Label.new("")
        self.header.set_xalign(0)
        context = self.header.get_style_context()
        context.add_class("challenge-header")
        content.pack_start(self.header, False, False, 0)
        self.load_css()

    def get_goal(self, **kwargs) -> str:
        """Callback; set this attribute in this parent class."""
        raise NotImplementedError

    def get_note(self, **kwargs) -> str:
        """Callback; set this attribute in this parent class."""
        raise NotImplementedError

    def get_verify_label(self, **kwargs) -> str:
        """Callback; set this attribute in this parent class."""
        raise NotImplementedError

    def make_grid_item(self, index, pixbuf, **kwargs) -> object:
        """Callback; set this attribute in this parent class."""
        raise NotImplementedError

    @property
    def formatted_goal(self):
        raw = str(self.get_goal())
        match = re.fullmatch(r"(.*)<strong>(.*)</strong>(.*)", raw)
        if not match:
            return html.escape(raw)
        groups = match.groups()
        return '{}<span size="xx-large">{}</span>{}'.format(
            *map(html.escape, [
                groups[0] and groups[0] + "\n",
                groups[1],
                groups[2],
            ]),
        )

    @classmethod
    def load_css(cls):
        if cls.css_provider is not None:
            return
        cls.css_provider = Gtk.CssProvider.new()
        cls.css_provider.load_from_data("""
            .challenge-button {
                border-radius: 0;
                border-width: 1px;
                padding: 0;
            }
            .challenge-check, .challenge-header {
                color: @theme_selected_fg_color;
                background-image: linear-gradient(
                    @theme_selected_bg_color, @theme_selected_bg_color);
            }
            .challenge-header {
                padding: 12px;
            }
            .challenge-check {
                border-radius: 50%;
            }
        """.encode("utf8"))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), cls.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def load_initial(self, image, *, rows, columns):
        self.columns = columns
        pixbuf = image_to_gdk_pixbuf(image)
        stride_x = image.width // columns
        stride_y = image.height // rows
        for i in range(rows * columns):
            column = i % columns
            row = i // columns
            cell_pixbuf = GdkPixbuf.Pixbuf.new(
                GdkPixbuf.Colorspace.RGB, pixbuf.get_has_alpha(),
                8, stride_x, stride_y,
            )
            src_x = stride_x * column
            src_y = stride_y * row
            pixbuf.copy_area(
                src_x, src_y, stride_x, stride_y, cell_pixbuf, 0, 0,
            )
            widget = self.make_grid_item(i, cell_pixbuf)
            context = widget.get_style_context()
            context.add_class("challenge-button")
            self.grid.attach(widget, column, row, 1, 1)
        self.content.pack_start(self.grid, True, True, 0)

    def get_grid_item(self, i):
        column = i % self.columns
        row = i // self.columns
        return self.grid.get_child_at(column, row)

    def replace_grid_item(self, i, new):
        column = i % self.columns
        row = i // self.columns
        old = self.grid.get_child_at(column, row)
        self.grid.remove(old)
        self.grid.attach(new, column, row, 1, 1)
        new.show_all()

    def update(self):
        goal = self.formatted_goal
        note = str(self.get_note())
        verify_label = str(self.get_verify_label())
        markup = goal + "\n"
        self.header.set_markup(markup + note)
        self.verify.set_label(verify_label)

    def run(self):
        self.show_all()
        response = super().run()
        self.destroy()
        while Gtk.events_pending():
            Gtk.main_iteration()
        if response != Gtk.ResponseType.OK:
            raise UserExit


class ChallengeToggleButton(Gtk.ToggleButton):
    def __init__(self, pixbuf):
        super().__init__()
        self.pixbuf = pixbuf
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        self.small_pixbuf = pixbuf.scale_simple(
            width * 0.9, height * 0.9, GdkPixbuf.InterpType.BILINEAR,
        )
        self.set_relief(Gtk.ReliefStyle.NONE)
        fixed = Gtk.Fixed.new()
        self.image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.image.set_size_request(width, height)
        self.check = Gtk.Image.new_from_icon_name(
            "object-select-symbolic", Gtk.IconSize.DND,
        )
        self.check.set_pixel_size(24)
        self.check.set_no_show_all(True)
        context = self.check.get_style_context()
        context.add_class("challenge-check")
        fixed.put(self.image, 0, 0)
        fixed.put(self.check, 0, 0)
        self.add(fixed)
        self.connect("toggled", lambda obj: self.toggle_check())

    def toggle_check(self):
        if self.get_active():
            self.check.show()
            self.image.set_from_pixbuf(self.small_pixbuf)
            return
        self.check.hide()
        self.image.set_from_pixbuf(self.pixbuf)


class BaseCaptchaDialog:
    def __init__(self):
        self.dialog = dialog = ChallengeDialogWidget()
        dialog.get_goal = self.__get_goal

    def __get_goal(self, **kwargs):
        return self.get_goal(**kwargs)

    def get_goal(self, **kwargs) -> str:
        """Callback; set this attribute in this parent class."""
        raise NotImplementedError

    def load_initial(self, image, *, rows, columns):
        self.dialog.load_initial(image, rows=rows, columns=columns)
        self.update()

    def update(self):
        self.dialog.update()

    def run(self):
        self.dialog.run()


class DynamicDialog(BaseCaptchaDialog):
    def __init__(self):
        super().__init__()
        dialog = self.dialog
        dialog.get_note = self.get_note
        dialog.get_verify_label = self.get_verify_label
        dialog.make_grid_item = self.make_grid_item

    def on_clicked(self, index, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def get_note(self, **kwargs):
        return "Click verify once there are none left"

    def get_verify_label(self, **kwargs):
        return "Ver_ify"

    def make_grid_item(self, index, pixbuf, **kwargs):
        button = Gtk.Button.new()
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        button.add(image)
        button.connect("clicked", lambda obj: self.handle_clicked(obj, index))
        context = button.get_style_context()
        context.add_class("challenge-button")
        return button

    def handle_clicked(self, button, index, **kwargs):
        spinner = Gtk.Spinner.new()
        spinner.set_size_request(32, 32)
        left = (button.get_allocated_width() - 32) / 2
        top = (button.get_allocated_height() - 32) / 2
        spinner.set_margin_top(math.floor(top))
        spinner.set_margin_left(math.floor(left))
        spinner.set_margin_bottom(math.ceil(top))
        spinner.set_margin_right(math.ceil(left))
        self.dialog.replace_grid_item(index, spinner)
        spinner.start()
        self.on_clicked(index)

    def replace_tile_image(self, index, image):
        pixbuf = image_to_gdk_pixbuf(image)
        spinner = self.dialog.get_grid_item(index)
        if pixbuf is None:
            spinner.stop()
            return
        button = self.make_grid_item(index, pixbuf)
        self.dialog.replace_grid_item(index, button)


class MultiCaptchaDialog(BaseCaptchaDialog):
    def __init__(self):
        super().__init__()
        self.selected = set()
        dialog = self.dialog
        dialog.get_note = self.get_note
        dialog.get_verify_label = self.get_verify_label
        dialog.make_grid_item = self.make_grid_item

    def get_note(self, **kwargs):
        note = "If there are none, click skip"
        if self.selected:
            note = '<span alpha="30%">{}</span>'.format(note)
        return note

    def get_verify_label(self, **kwargs):
        if self.selected:
            return "Ver_ify"
        return "Sk_ip"

    def make_grid_item(self, index, pixbuf, **kwargs):
        button = ChallengeToggleButton(pixbuf)
        button.connect(
            "toggled", lambda obj: self.handle_toggled(obj, index),
        )
        return button

    def handle_toggled(self, button, index, **kwargs):
        if button.get_active():
            self.selected.add(index)
        else:
            self.selected.remove(index)
        self.update()

    def run(self):
        super().run()
        return list(self.selected)


class GuiSolver:
    def __init__(self, solver, gui: "Gui"):
        self.solver = solver
        self.gui: "Gui" = gui
        self.dialog = None

    def get_goal(self, **kwargs):
        return self.gui.goal

    def prepare_dialog(self, dialog):
        dialog.get_goal = self.get_goal
        return dialog

    def run(self):
        self.solver.run()


class GuiDynamicSolver(GuiSolver):
    def __init__(self, solver, gui):
        super().__init__(solver, gui)
        solver.on_initial_image = self.handle_initial_image
        solver.on_tile_image = self.handle_tile_image
        self.lock = RLock()

    def handle_initial_image(self, image, **kwargs):
        solver = self.solver
        rows, columns = solver.dimensions
        self.dialog = self.prepare_dialog(DynamicDialog())
        self.dialog.on_clicked = self.handle_gui_tile_clicked
        self.dialog.load_initial(image, rows=rows, columns=columns)
        self.dialog.run()
        print("Submitting solution...")
        solver.finish()

    # Called from a non-UI thread.
    def handle_tile_image(self, index, image, **kwargs):
        def callback():
            self.dialog.replace_tile_image(index, image)
        GLib.timeout_add(0, callback)

    def handle_gui_tile_clicked(self, index):
        def target():
            with self.lock:
                self.solver.select_tile(index)
        Thread(target=target, daemon=True).start()


class GuiMultiCaptchaSolver(GuiSolver):
    def __init__(self, solver, gui):
        super().__init__(solver, gui)
        solver.on_image = self.handle_image

    def handle_image(self, image, **kwargs):
        solver = self.solver
        rows, columns = solver.dimensions
        self.dialog = self.prepare_dialog(MultiCaptchaDialog())
        self.dialog.load_initial(image, rows=rows, columns=columns)
        indices = self.dialog.run()
        print("Submitting solution...")
        solver.select_indices(indices)


class Gui(Frontend):
    def __init__(self, recaptcha):
        super().__init__(recaptcha)
        self.goal = None
        self._first = True
        rc = self.rc
        rc.on_goal = self.handle_goal
        rc.on_challenge = self.handle_challenge
        rc.on_challenge_dynamic = self.challenge_dynamic
        rc.on_challenge_multicaptcha = self.challenge_multicaptcha
        rc.on_challenge_blocked = self.challenge_blocked
        rc.on_challenge_unknown = self.challenge_unknown

    def handle_goal(self, goal, meta, raw, **kwargs):
        if not raw:
            print("WARNING: Could not determine challenge objective.")
            raw = json.dumps(meta)
        self.goal = raw

    def handle_challenge(self, ctype, **kwargs):
        if not self._first:
            print("You must solve another challenge.")
            print()
        self._first = False

    def challenge_dynamic(self, solver, **kwargs):
        GuiDynamicSolver(solver, self).run()

    def challenge_multicaptcha(self, solver, **kwargs):
        GuiMultiCaptchaSolver(solver, self).run()

    def challenge_blocked(self, ctype, **kwargs):
        Cli.raise_challenge_blocked(ctype)

    def challenge_unknown(self, ctype, **kwargs):
        Cli.raise_challenge_unknown(ctype)
