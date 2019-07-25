==============
django-giftbox
==============

.. image:: https://www.travis-ci.org/bwhicks/django-giftbox.svg?branch=master
    :target: https://www.travis-ci.org/bwhicks/django-giftbox
    :alt: Travis-CI badge

.. image:: https://codecov.io/gh/bwhicks/django-giftbox/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bwhicks/django-giftbox
    :alt: Codecov.io badge


Description
-----------

django-giftbox is an app for the Django web framework that provides an easy
wrapper for X-Sendfile functionality in Apache.

This lets users protect files by not allowing them to be downloaded
directly, but allows Django to programmatically send a redirect and let the
webserver handle the transaction.

The current implementation is compatible with Django 1.11+ (tested against LTS
releases including 2.2) and py2/3 compatible.

The only required dependency is Django itself and mod_xsendfile_ installed for 
Apache.

.. _mod_xsendfile: https://tn123.org/mod_xsendfile/

Installation
------------

You can simply download from PyPi using pip::

  pip install django-giftbox

To install extra ``python-magic`` functionality::

  pip install django-giftbox[magic]

You'll need to have ``libmagic`` (or ``libmagic-dev`` on many Linux distributions) 
installed to use this, otherwise ``python-magic`` will break.

Or feel free to clone from the ``master`` branch::

    pip install git+https://github.com/bwhicks/django-giftbox.git@master#egg=giftbox

That's it.

Configuration
-------------

There are two 'modes' for giftbox. One of them is ``dev``, and this is the
default when running using the Django development server. Giftbox should auto-detect
this and run accordingly.

The other is ``prod``, which assumes you are routing your Django appplication through
a web server like Apache

In Django ``settings.py``, define a dictionary called ``GIFTBOX_SETTINGS``.
You must define ``doc_root``, which is the directory
where the files you wish t
Usageo serve via Giftbox are located. This can be a relative
path under your vhost's doc root or an absolute file path.

You can also specify these at run time, but you must least have ``GIFTBOX_SETTINGS``
with some sane defaults for one of those settings::

  GIFTBOX_SETTINGS = {
    'type': 'prod',  # will still detect dev server locally
    'doc_root': '/path/to/protected/files',
  }

A corresponding Apache entry in a Vhost or other configuration would be::

  XSendFile on
  XSendFilePath /path/to/protected/files

The major advantage of this is that you can block regular access to this path
or leave it out of Apache's docroot.


Optional python-magic
=====================

If ``libmagic`` and ``python-magic`` are installed, Giftbox will set the
``Content-Type`` header when passing information to your HTTP server. If you
don't want this functionality (serving many files quickly or large ones), you can
disable it and your HTTP server's mime handling will apply::

  GIFTBOX_SETTINGS = {
    # other settings...
    'use_magic': False,
  }


=====

In a view or view function, create an instance as follows::

  from gitfbox import GiftBox

  def my_view_func(request):
    box = GiftBox(request)
    return box.send('filename')


``box`` in this case is an instance of ``GiftBox``, which can have its ``self.kwargs``
dict modified in any way, as well as having ``kwargs`` passed via its constructor.
By default it looks to ``settings.py`` for its defaults.

``box.send()`` returns an instance of ``django.httpd.HttpReponse``
(or ``FileResponse``) with
appropriate headers set and ``Content-Type`` cleared so that your web server
can use its own MIME handling to set the type appropriately (unless you use
the optional ``python-magic`` functionality). You can manually
specify this before returning the ``HttpResponse`` object, too.

All of this depends on a correct server setup for Apache that
properly creates a protected url that allows sendfile type requests.

The object allows flexible settings of virtually every kwarg at any point. If
you need to set the  `doc_root`` dynamically, either when you
instantiate the box or when you call ``Giftbox.send()``, you can do that.

Tests
=====

All tests can be run using ``tox`` or ``python setup.py pytest``.
