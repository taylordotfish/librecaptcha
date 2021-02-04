librecaptcha
============

Version 0.6.4

librecaptcha is a free/libre program and library that allows you to solve
`reCAPTCHA`_ challenges.

*librecaptcha does not automatically solve challenges and is not designed to
make it easier to do so—it provides an interface through which a human can
solve the challenges without proprietary software.*

.. _reCAPTCHA: https://en.wikipedia.org/wiki/ReCAPTCHA


Installation
------------

From PyPI
~~~~~~~~~

Install with `pip`_::

    sudo pip3 install librecaptcha[gtk]

To install locally, run without ``sudo`` and add the ``--user`` option.
You can omit ``[gtk]`` if you don’t want to install the GTK 3 GUI.


From the Git repository
~~~~~~~~~~~~~~~~~~~~~~~

Clone the repository with the following commands (you’ll need to have `Git`_
installed)::

    git clone https://github.com/taylordotfish/librecaptcha
    cd librecaptcha

Then install with `pip`_::

    sudo pip3 install .[gtk]

To install locally, run without ``sudo`` and add the ``--user`` option.
You can omit ``[gtk]`` if you don’t want to install the GTK 3 GUI.


Run without installing
~~~~~~~~~~~~~~~~~~~~~~

Run the first set of commands in the previous section to clone the repository.
Then, install the required dependencies by running::

    sudo pip3 install -r requirements.txt

To install the dependencies locally, run without ``sudo`` and add ``--user``.

.. _pip: https://pip.pypa.io
.. _Git: https://git-scm.com


Usage
-----

If you installed librecaptcha, you can simply run ``librecaptcha``.
Otherwise, run ``./librecaptcha.py``. Pass the ``--help`` option to show usage
information. If you’d like to use the GUI, be sure to pass the ``--gui``
option.

To use librecaptcha programmatically, import it::

    import librecaptcha

and then call ``librecaptcha.get_token()``. Its signature is::

    get_token(
        api_key: str,
        site_url: str,
        user_agent: str, *,
        gui=False,
        debug=False,
    ) -> str

Parameters:

* ``api_key``:
  The reCAPTCHA API key to use. This is usually the value of the
  ``data-sitekey`` HTML attribute.

* ``site_url``:
  The base URL of the site that contains the reCAPTCHA challenge. This should
  start with ``http://`` or ``https://`` and include the hostname. Everything
  after the hostname is optional. For example: ``https://example.com``

* ``user_agent``:
  The user-agent string to use. This should match the user-agent used when
  sending the request that requires a reCAPTCHA token. You can generate a
  random user-agent string with ``librecaptcha.random_user_agent()``.

* ``gui``:
  Whether to use the GTK 3 GUI (as opposed to the CLI). The CLI writes to
  standard output and reads from standard input.

* ``debug``:
  Whether to print debug information.

Returns: A reCAPTCHA token. This should usually be submitted with the form as
the value of the ``g-recaptcha-response`` field. These tokens usually expire
after a couple of minutes.


Notes
-----

librecaptcha currently supports two types of challenges: *dynamic* and
*multicaptcha*.

*dynamic* challenges present you with a grid of different images and ask you to
select the images that match the given description. Each time you click an
image, a new one takes its place. Usually, three images from the initial
set match the description, and at least one of the replacement images does as
well.

*multicaptcha* challenges present you with one large image split into a grid
of tiles and ask you to select the tiles that contain a given object.
Occasionally, the image will not contain the object, but rather something that
looks similar. It is possible to select no tiles in this case, but reCAPTCHA
may have been fooled by the similar-looking object and would reject a selection
of no tiles.


Known issues
------------

Even when all challenges are completed and a token is obtained, the token may
still be rejected when used. If this happens, simply try again. Waiting a
while, using a computer on a different network, or using a different user-agent
string may also help. Unfortunately, you may have to try many times—perhaps
dozens or more.


What’s new
----------

Version 0.6.3:

* librecaptcha should now work again, aside from the existing issues with
  tokens sometimes being rejected.

Version 0.6.0:

* Added ``librecaptcha.has_gui()``, which returns whether the GUI can be used.
* Improved cross-platform support for the CLI.

Version 0.5.0:

* Added a GTK 3 GUI (thanks, cyclopsian!).
* ``get_token()`` now has an optional ``gui`` parameter.
* ``get_token()`` now requires a user-agent string.
* ``librecaptcha.py`` now has a ``--gui`` option.
* ``librecaptcha.py`` now accepts an optional ``<user-agent>`` argument.
  If not provided, a random user-agent string is chosen and shown.

Version 0.4.0:

* Image windows are now automatically closed when questions are answered.

Version 0.3.x:

* Fixed possible encoding issue in ``setup.py``.
* librecaptcha can now be installed from PyPI, or from the Git repository with
  pip or ``setup.py``.

Version 0.2.x:

* Updated user-agent list.
* The current reCAPTCHA version is now fetched during initialization and no
  longer needs to be manually updated.


Dependencies
------------

* `Python`_ ≥ 3.5
* The following Python packages:

  - `Pillow`_
  - `requests`_
  - `slimit`_
  - `PyGObject`_ (only for GUI)

The installation instructions above handle installing the Python packages.
Alternatively, running ``pip3 install -r requirements.freeze.txt`` will install
specific versions of the dependencies that have been confirmed to work.

.. _Python: https://www.python.org/
.. _Pillow: https://pypi.org/project/Pillow/
.. _requests: https://pypi.org/project/requests/
.. _slimit: https://pypi.org/project/slimit/
.. _PyGObject: https://pypi.org/project/PyGObject/


License
-------

librecaptcha is licensed under the GNU General Public License, version 3 or
any later version. See `LICENSE`_.

This README file has been released to the public domain using `CC0`_.

.. _LICENSE: LICENSE
.. _CC0: https://creativecommons.org/publicdomain/zero/1.0/
