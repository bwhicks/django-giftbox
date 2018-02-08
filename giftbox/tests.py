import os
import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from .box import GiftBox
from .wrappers import send_dev_server, xsendfile, get_mime
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch


class TestGiftBox(TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.gbs = settings.GIFTBOX_SETTINGS

    def test_init(self):
        g = GiftBox(self.request)
        assert isinstance(g, GiftBox)
        assert g.request == self.request
        assert g.wrapper == xsendfile
        assert g.kwargs['sendfile_url'] == '/protected/'
        assert g.kwargs['doc_root'] == 'foo'

    def test_force_dev_server(self):
        self.request.META.get.return_value = 'WSGIServer'
        g = GiftBox(self.request)
        assert g.wrapper == send_dev_server

    def test_no_gbs(self):
        with self.settings(GIFTBOX_SETTINGS=None):
            with pytest.raises(ImproperlyConfigured):
                g = GiftBox(self.request)

    def test_type(self):
        gbs = self.gbs.copy()
        gbs['type'] = 'dev'
        with self.settings(GIFTBOX_SETTINGS=gbs):
            g = GiftBox(self.request)
            assert g.wrapper == send_dev_server
        gbs['type'] = 'prod'
        with self.settings(GIFTBOX_SETTINGS=gbs):
            g = GiftBox(self.request)
            assert g.wrapper == xsendfile

    def test_assign_none_sendfile_doc_root(self):
        gbs = self.gbs.copy()
        gbs['type'] = 'prod'
        gbs['sendfile_url'] = None
        gbs['doc_root'] = None
        with self.settings(GIFTBOX_SETTINGS=gbs):
            g = GiftBox(self.request)
            assert not g.kwargs['sendfile_url']
            assert not g.kwargs['doc_root']

    def test_kwarg_overrides(self):
        kwargs = {
            'sendfile_url': 'bar',
            'doc_root': 'baz'
        }
        g = GiftBox(self.request, **kwargs)
        assert g.kwargs['sendfile_url'] == 'bar'
        assert g.kwargs['doc_root'] == 'baz'

    @patch('giftbox.wrappers.HttpResponse')
    @patch('giftbox.wrappers.serve')
    def test_send_no_magic(self, mockhttpresponse, testserve):
        mockhttpresponse = {'Content-Type': ''}
        g = GiftBox(self.request)
        g.send('foo', use_magic=False)
        g.wrapper = None
        with pytest.raises(ImproperlyConfigured):
            g.send('foo')

        g.wrapper = send_dev_server
        g.kwargs['doc_root'] = None
        with pytest.raises(ImproperlyConfigured):
            g.send('foo')

        del g.kwargs['sendfile_url']
        g.wrapper = xsendfile
        with pytest.raises(ImproperlyConfigured):
            g.send('foo')

    @patch('giftbox.box.GiftBox.send')
    def test_send_call(self, mocksend):
        g = GiftBox(self.request)
        g.send('foo', bar='baz')

        assert mocksend.called
        mocksend.assert_called_with('foo', bar='baz')

    @patch('giftbox.box.send_dev_server')
    @patch('giftbox.box.xsendfile')
    def test_pass_kwargs(self, dev, sendfile):
        g = GiftBox(self.request)
        g.send('foo', doc_root='foobar')
        assert g.kwargs['doc_root'] == 'foobar'


class TestWrappersNoMagic(TestCase):

    def setUp(self):
        self.request = MagicMock()

    @patch('giftbox.wrappers.serve')
    def test_send_dev_server(self, mockserve):
        mockserve.return_value = {'Content-Type': ''}
        res = send_dev_server(self.request, 'foo', doc_root='bar',
                              use_magic=False)
        assert mockserve.called
        assert res['Content-Disposition'] == 'attachment; filename=foo'

    @patch('giftbox.wrappers.HttpResponse')
    def test_xsendfile(self, fakeresponse):
        fakeresponse.return_value = {'Content-Type': ''}
        res = xsendfile(self.request, 'foo', sendfile_url='/bar/',
                        use_magic=False)
        assert fakeresponse.called
        fakeresponse.assert_called_with()
        assert res['X-Sendfile'] == '/bar/foo'
        assert res['X-Accel-Redirect'] == '/bar/foo'


class TestWrappersMagic(TestCase):

    def setUp(self):
        self.request = MagicMock()

    def test_get_mime(self):

        testfile = open('foo.txt', 'w')
        testfile.write('This is a text file\n')
        testfile.close()
        mime = get_mime('foo.txt')
        os.remove('foo.txt')
        assert mime == 'text/plain'

    @patch('giftbox.wrappers.GOT_MAGIC')
    @patch('giftbox.wrappers.get_mime')
    @patch('giftbox.wrappers.serve')
    def test_send_dev_server(self, mockserve, mockmime, mockflag):
        mockflag.return_value = True
        mockserve.return_value = {'Content-Type': ''}
        mockmime.return_value = 'text/foo'
        res = send_dev_server(self.request, 'foo', doc_root='bar',
                              use_magic=True)
        assert mockserve.called
        assert res['Content-Disposition'] == 'attachment; filename=foo'
        assert res['Content-Type'] == 'text/foo'
        mockmime.assert_called_with('bar/foo')

    @patch('giftbox.wrappers.GOT_MAGIC')
    @patch('giftbox.wrappers.get_mime')
    @patch('giftbox.wrappers.HttpResponse')
    def test_xsendfile(self, fakeresponse, mockmime, mockflag):

        mockflag.return_value = True
        fakeresponse.return_value = {'Content-Type': ''}
        mockmime.return_value = 'text/foo'
        res = xsendfile(self.request, 'foo', sendfile_url='/bar/',
                        use_magic=True, doc_root='/baz/bam')
        assert fakeresponse.called
        assert res['X-Sendfile'] == '/bar/foo'
        assert res['X-Accel-Redirect'] == '/bar/foo'
        assert res['Content-Type'] == 'text/foo'

        with pytest.raises(ImproperlyConfigured):
            res = xsendfile(self.request, 'foo', sendfile_url='/bar/',
                            use_magic=True)
