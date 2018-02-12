librecaptcha
============

Version 0.2.2

librecaptcha is a free/libre program and library that allows you to solve
[reCAPTCHA] challenges.

*This does not automatically solve challenges. It provides an interface through
which a human can solve them.*

[reCAPTCHA]: https://en.wikipedia.org/wiki/ReCAPTCHA


Installation
------------

Run the following commands (you will need to have [Git] installed):

```
git clone https://github.com/taylordotfish/librecaptcha
cd librecaptcha
```

Then, to install the required Python packages, you can either run:

```
sudo pip3 install -r requirements.txt
```

to install the packages globally, or you can run:

```
pip3 install --user -r requirements.txt
```

to install them locally.

[Git]: https://git-scm.com


Usage
-----

Run ``./librecaptcha.py`` for usage information.

To use librecaptcha programmatically, make sure this repository (or whatever
the parent directory of the “librecaptcha” package is) is in
[Python’s path][0]. Your program can then run
``from librecaptcha import get_token`` and call the ``get_token()`` function.

The signature of ``get_token()`` is:

```
get_token(api_key, site_url, debug=False, user_agent=None)
```

Parameters:

* ``api_key`` (string): The reCAPTCHA API key to use.
* ``site_url`` (string): The base URL of the site that contains the reCAPTCHA
  challenge. This should start with “http://” or “https://” and include the
  hostname, but nothing else. For example, “[https://example.com:443][1]”.
* ``debug`` (bool): Whether or not to print debug information.
* ``user_agent`` (string): The user-agent string to use. If not specified, a
  random one will be used.

Returns (string): A reCAPTCHA token. This should usually be submitted with the
form as the value of the “g-recaptcha-response” field. (Note: these tokens
usually expire after a couple of minutes.)

[0]: https://docs.python.org/3/library/sys.html#sys.path
[1]: https://example.com:443


What’s new
----------

Version 0.2.2:

* Cleaned up some code.

Version 0.2.1:

* Updated user-agent list.

Version 0.2.0:

* The current reCAPTCHA version is now fetched during initialization and no
  longer needs to be manually updated.


Dependencies
------------

* [Python] ≥ 3.4
* The following Python packages (these can be installed from
  [requirements.txt](requirements.txt); see the [Installation] section):
  - [Pillow] ≥ 4.1.1
  - [requests] ≥ 2.18.1
  - [slimit] ≥ 0.8.1

[Installation]: #installation
[Python]: https://www.python.org/
[Pillow]: https://pypi.python.org/pypi/Pillow/
[requests]: https://pypi.python.org/pypi/requests/
[slimit]: https://pypi.python.org/pypi/slimit/


License
-------

librecaptcha is licensed under the GNU General Public License, version 3 or
any later version. See [LICENSE].

This README file has been released to the public domain using [CC0].

[LICENSE]: LICENSE
[CC0]: https://creativecommons.org/publicdomain/zero/1.0/
