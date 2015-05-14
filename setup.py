from setuptools import setup
from setuptools.command.install import install

import stat
import hashlib
import os
import tempfile
import urllib
import shutil
import zipfile


class InstallGaeSDK(install):
    GAE_VERSION = '1.9.20'
    GAE_SHA1SUM = '8fce499b99a60bd983aea39255ef5442273e5b3a'
    SDK_FILE = 'google_appengine_1.9.20.zip'
    GAE_URL = (
        'https://storage.googleapis.com/appengine-sdks/featured/' + SDK_FILE)

    @property
    def _gae_zip(self):
        return 'google_appengine_{}.zip'.format(self.GAE_VERSION)

    @property
    def _gae_url(self):
        return 'https://storage.googleapis.com/appengine-sdks/featured/' + \
            self._gae_zip

    def _download_appengine(self, tmp_dir):
        tmp_file = os.path.join(tmp_dir, self.SDK_FILE)
        print "Downloading to {}".format(tmp_file)

        req = urllib.urlopen(self._gae_url)

        with open(tmp_file, 'wb') as f:
            shutil.copyfileobj(req, f)
        return tmp_file

    def _verify_file(self, gae_zip):
        print "Verifying download..."
        with open(gae_zip, 'rb') as fp:
            sha1sum = hashlib.sha1(fp.read()).hexdigest()
        assert sha1sum == self.GAE_SHA1SUM

    def _decompress(self, gae_zip):
        with zipfile.ZipFile(gae_zip) as zf:
            zf.extractall(self.install_lib)

    def _write_pth(self):
        p = os.path.join(self.install_lib, 'gae_setuptools.pth')
        with open(p, 'w') as f:
            f.write(os.path.join(self.install_lib, 'google_appengine'))
            f.write('\nimport gae_setuptools')
        return p

    def _fix_bin(self):
        for f in ['dev_appserver.py', 'appcfg.py']:
            path = os.path.join(self.install_lib, 'google_appengine', f)
            s = os.stat(path)
            os.chmod(path, s.st_mode | stat.S_IXUSR | stat.S_IXGRP)

    def run(self):
        install.run(self)
        tmp_dir = tempfile.mkdtemp()
        try:
            zip_pth = self._download_appengine(tmp_dir)
            self._verify_file(zip_pth)
            self._decompress(zip_pth)
            self._write_pth()
            self._fix_bin()
        finally:
            print "Cleaning up temp directory {}".format(tmp_dir)
            shutil.rmtree(tmp_dir)


setup(
    name='gae_setuptools',
    packages=[],    # this must be the same as the name above
    py_modules=['gae_setuptools'],
    version=InstallGaeSDK.GAE_VERSION,
    description='Install GAE SDK to a virtualenv with pip',
    author='Chris Targett',
    author_email='chris@xlevus.net',
    keywords=['google appengine'],
    classifiers=[],
    cmdclass={
        'install': InstallGaeSDK,
    },
)
