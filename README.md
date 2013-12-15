============
Installation
============

* Add ``'cosinnus_etherpad'`` to ``INSTALLED_APPS``
* Add the following settings:
``
  COSINNUS_ETHERPAD_API_KEY = '<your API key>'
  COSINNUS_ETHERPAD_BASE_URL = '<your pad server url>'
``
Note that the webserver running the etherpad app has to be in the same domain
as the etherpad server, e.g. http://web.yourdomain.com runs cosinnus and
http://pad.yourdomain.com runs the etherpad server.
* For tests to work, you need to have a running etherpad server configured in
tests/settings/base.py
