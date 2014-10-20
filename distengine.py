import site
from dev_appserver import EXTRA_PATHS
for pth in EXTRA_PATHS:
    site.addsitedir(pth)
