"""
Package that enables Django to easily and quickly be configured to pass
X-Sendfile or X-Accel-Redirect requests to web servers for files that need to
have some sort of permimssions check run prior to serving.
"""

from .box import GiftBox


__version_info__ = (0, 5, 0)
__version__ = '.'.join(str(num) for num in __version_info__)
