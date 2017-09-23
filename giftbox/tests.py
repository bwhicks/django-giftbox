from django.test import TestCase
from giftbox import GiftBox

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

class TestBasics(TestCase):

    def test_init(self):
        request = MagicMock()
        META = MagicMock()
        META.get.return_value = 'foo'
        request.META.return_value = META
        g = GiftBox(request)
        assert isinstance(g, GiftBox)
