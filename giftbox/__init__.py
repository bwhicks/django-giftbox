"""
Package that enables Django to easily and quickly be configured to pass
X-Sendfile or X-Accel-Redirect requests to web servers for files that need to
have some sort of permimssions check run prior to serving.
"""

from .box import GiftBox

from .version import __version__, version_info
