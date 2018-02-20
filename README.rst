librecaptcha
============

Version 0.3.5-dev

librecaptcha is a free/libre program and library that allows you to solve
`reCAPTCHA`_ challenges.

*This does not automatically solve challenges. It provides an interface through
which a human can solve them.*

.. _reCAPTCHA: https://en.wikipedia.org/wiki/ReCAPTCHA


Installation
------------

From PyPI
~~~~~~~~~

Install with `pip`_::

    sudo pip3 install librecaptcha

To install locally, run without ``sudo`` and add the ``--user`` option.


From the Git repository
~~~~~~~~~~~~~~~~~~~~~~~

Clone the repository with the following commands (you’ll need to have `Git`_
installed)::

    git clone https://github.com/taylordotfish/librecaptcha
    cd librecaptcha

Then install with `pip`_::

    sudo pip3 install .

Alternatively, you can run::

    sudo ./setup.py install

With either command, to install locally, run without ``sudo`` and add the
``--user`` option.

Run without installing
~~~~~~~~~~~~~~~~~~~~~~

Run the first set of commands in the previous section to clone the repository.
Then, install the required dependencies by running::

    sudo pip3 install -r requirements.txt

To install the dependencies locally, run without ``sudo`` and add the
``--user`` option.

.. _pip: https://pip.pypa.io
.. _Git: https://git-scm.com


Usage
-----

If you installed librecaptcha, you can simply run ``librecaptcha``.
Otherwise, run ``./librecaptcha.py``. This will show usage information.

To use librecaptcha programmatically, import it::

    from librecaptcha import get_token

and then call the ``get_token()`` function. Its signature is::

    get_token(api_key, site_url, debug=False, user_agent=None)

Parameters:

* ``api_key`` (str): The reCAPTCHA API key to use.
* ``site_url`` (str): The base URL of the site that contains the reCAPTCHA
  challenge. This should start with ``http://`` or ``https://`` and include the
  hostname, but nothing else. For example, ``https://example.com``.
* ``debug`` (bool): Whether or not to print debug information.
* ``user_agent`` (str): The user-agent string to use. If not specified, a
  random one will be used.

Returns (str): A reCAPTCHA token. This should usually be submitted with the
form as the value of the ``g-recaptcha-response`` field. (Note: These tokens
usually expire after a couple of minutes.)


What’s new
----------

Version 0.3.4:

* Fixed possible encoding issue in ``setup.py``.

Version 0.3.3:

* librecaptcha can now be installed from PyPI, or from the Git repository with
  pip or ``setup.py``.

Version 0.2.x:

* Updated user-agent list.
* The current reCAPTCHA version is now fetched during initialization and no
  longer needs to be manually updated.


Dependencies
------------

* `Python`_ ≥ 3.4
* The following Python packages (the installation instructions above handle
  installing these):

  - `Pillow`_ ≥ 4.1.1
  - `requests`_ ≥ 2.18.1
  - `slimit`_ ≥ 0.8.1

.. _Python: https://www.python.org/
.. _Pillow: https://pypi.python.org/pypi/Pillow/
.. _requests: https://pypi.python.org/pypi/requests/
.. _slimit: https://pypi.python.org/pypi/slimit/


License
-------

librecaptcha is licensed under the GNU General Public License, version 3 or
any later version. See `LICENSE`_.

This README file has been released to the public domain using `CC0`_.

.. _LICENSE: LICENSE
.. _CC0: https://creativecommons.org/publicdomain/zero/1.0/
