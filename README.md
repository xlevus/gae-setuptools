GAE Setuptools
==============

A solution to https://code.google.com/p/googleappengine/issues/detail?id=10822

Provides a quick setuptools hack that'll download and install the Google App Engine SDK to your virtual environment.


Usage
-----
```bash
pip install git+https://github.com/xlevus/gae-setuptools.git
```

Known Issues
------------

 * Google removes old versions of releases, causing 404s
 * Uninstalling the package won't remove the `google_appengine` or `gae_setuptools.pth` file.
 * I have no idea what I'm doing (But it works, mostly).

