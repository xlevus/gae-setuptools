GAE Setuptools
==============

A dirty little setuptools hack that'll install the Google App Engine SDK

An alternative solution to https://code.google.com/p/googleappengine/issues/detail?id=10822

Usage
-----
```bash
pip install git+https://github.com/xlevus/gae-setuptools.git
```

Known Issues
------------

 * Google removes their old versions from their servers causing 404s
 * Uninstalling the package won't remove the `google_appengine` or `gae_setuptools.pth` file.
