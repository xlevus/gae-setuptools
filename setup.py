from setuptools import setup
from setuptools.command.install import install

import hashlib
import os
import subprocess
import tempfile
import urllib
import shutil
import zipfile

GAE_FILE = 'google_appengine_1.9.12.zip'
GAE_SHA1SUM = ''
GAE_URL = 'https://storage.googleapis.com/appengine-sdks/featured/' + GAE_FILE


def after_install(options, home_dir):
    """Setup the GAE SDK.

    Download and unzip to home_dir/google_appengine
    Create .pth files for each in `lib/python2.7/site-packages/`.
    """
    # Create a secure temp directory.
    tmp_dir = tempfile.mkdtemp(dir=home_dir)
    tmp_file = os.path.join(tmp_dir, GAE_FILE)
    print 'Downloading', GAE_FILE, 'to', tmp_dir

    # Download the SDK with curl into the temp directory.
    subprocess.call(['curl', GAE_URL, '-o', tmp_file])

    # Calculate the SHA1 sum of the file.
    with open(tmp_file, 'rb') as fp:
        sha1sum = hashlib.sha1(fp.read()).hexdigest()

    # Compare the SHA1 sum and fail on mismatch.
    try:
        assert GAE_SHA1SUM == sha1sum
    except AssertionError:
        print 'SHA1SUM mismatch'
        print GAE_SHA1SUM, '!=', sha1sum
        print '1) The GAE SDK version was changed in', __file__, ' and the SHA1SUM was not, or'
        print '2) The downloaded .zip file is compromised.'
        raise

    # Unzip the SDK.
    subprocess.call(['unzip', '-o', tmp_file, '-d', home_dir])

    # Clean up the temp file and directory.
    os.remove(tmp_file)
    os.rmdir(tmp_dir)

    # Create .pth files.
    site_pkg_dir = os.path.join(home_dir, 'lib', 'python2.7', 'site-packages')
    gae_dir = os.path.join(home_dir, 'google_appengine')
    fancy_urllib_dir = os.path.join(gae_dir, 'lib', 'fancy_urllib')

    # Write google_appengine.pth
    fp = open(os.path.join(site_pkg_dir, 'google_appengine.pth'), 'w')
    fp.write(PTH_TPL % {'path': os.path.abspath(gae_dir)})
    fp.close()

    # Write fancy_urllib.pth
    fp = open(os.path.join(site_pkg_dir, 'fancy_urllib.pth'), 'w')
    fp.write(PTH_TPL % {'path': os.path.abspath(fancy_urllib_dir)})
    fp.close()


class CustomInstallCommand(install):
    GAE_VERSION = '1.9.13'
    GAE_SHA1SUM = '05166691108caddc4d4cfdf683cfc4748df197a2'

    SDK_FILE = 'google_appengine_1.9.13.zip'

    @property
    def _gae_zip(self):
        return 'google_appengine_{}.zip'.format(self.GAE_VERSION)

    @property
    def _gae_url(self):
        return 'https://storage.googleapis.com/appengine-sdks/featured/' + \
            self._gae_zip

    def _download_appengine(self, tmp_dir):
        tmp_file = os.path.join(tmp_dir, GAE_FILE)
        print "Downloading to {}".format(tmp_file)

        req = urllib.urlopen(self._gae_url)

        with open(tmp_file, 'wb') as f:
            shutil.copyfileobj(req, f)
        return tmp_file

    def _verify_file(self, gae_zip):
        print "Verifying download..."
        with open(gae_zip, 'rb') as fp:
            sha1sum = hashlib.sha1(fp.read()).hexdigest()
            print fp.tell()
        assert sha1sum == self.GAE_SHA1SUM

    def _decompress(self, gae_zip):
        with zipfile.ZipFile(gae_zip) as zf:
            zf.extractall(self.install_lib)

    def _write_pth(self):
        with open(os.path.join(self.install_lib, 'distengine.pth'), 'w') as f:
            f.write(os.path.join(self.install_lib, 'google_appengine'))
            f.write('\nimport distengine')

    def run(self):
        install.run(self)
        tmp_dir = tempfile.mkdtemp()
        try:
            #zip_pth = self._download_appengine(tmp_dir)
            #self._verify_file(zip_pth)
            self._decompress(self.SDK_FILE)
            self._write_pth()
        finally:
            print "Cleaning up temp directory {}".format(tmp_dir)
            shutil.rmtree(tmp_dir)


setup(
    name='distengine',
    packages=[],    # this must be the same as the name above
    py_modules=['distengine'],
    version='0.1',
    description='A random test lib',
    author='Peter Downs',
    author_email='peterldowns@gmail.com',
    keywords=['appengine'],
    classifiers=[],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
