==============
django-giftbox
==============

.. image:: https://www.travis-ci.org/bwhicks/django-giftbox.svg?branch=develop
    :target: https://www.travis-ci.org/bwhicks/django-giftbox

.. image:: https://codecov.io/gh/bwhicks/django-giftbox/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/bwhicks/django-giftbox


Description
-----------

django-giftbox is an app for the Django web framework that provides an easy
wrapper for xsendfile / x-accel-http functionality in Apache / lighthttp /
nginx. This lets users protect files by not allowing them to be downloaded
directly, but allows Django to programmatically send a redirect and let the
webserver handle the transaction.

Eventually this package will also provide other convenience functions for
protected file setups and Django.

The current implementation is compatible with Django 1.8+ (tested against LTS
releases) and py2/3 compatible. The only depedency is Django itself.

Installation
------------

Hopefully this will be released to pypi. Until such time, however, you can
clone from ``master`` or ``develop`` branches.

To install via ``pip``, use something like this::

    pip install git+https://github.com/bwhicks/django-giftbox.git@master#egg=giftbox

That's it.

Configuration
-------------

There are two 'modes' for giftbox. One of them is ``dev``, and this is the
default when running using the Django development server. Giftbox should auto-detect
this and run accordingly.

The other is ``prod``, which assumes you are routing your Django appplication through
a web server like Apache or nginx.

In Django ``settings.py``, define a dictionary called ``GIFTBOX_SETTINGS``.
For the development server, you must define ``doc_root``, which is the directory
where the files you wish to serve via Giftbox are located. For ``prod``, you will
need to set the url on which your webserver will listen and answer
``Sendfile`` or ``x-accel-http`` headers as ``sendfile_url``.

You can also specify these at run time, but you must least have ``GIFTBOX_SETTINGS``
with some sane defaults for one of those settings. If you'd like to run this
on a dev server, you absolutely must define the ``doc_root`` key. An example::

  GIFTBOX_SETTINGS = {
    'type': 'prod', # will still detect dev server locally
    'doc_root': '/path/to/protected/files',
    'sendfile_url': '/protected/url/',
  }

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


Usage
-----

In a view or view function, create an instance as follows::

  from gitfbox import GiftBox

  def my_view_func(request):
    box = GiftBox(request)
    return box.send('file.name')


``box`` in this case is an instance of ``GiftBox``, which can have its ``self.kwargs``
dict modified in any way, as well as having ``kwargs`` passed via its constructor.
By default it looks to ``settings.py`` for its defaults.

``box.send()`` returns an instance of ``django.httpd.HttpReponse`` with
appropriate headers sent and ``Content-Type`` cleared so that your web server
can use its own MIME handling to set the type appropriately. You can manually
specify this before returning the ``HttpResponse`` object, too.

All of this depends on a correct server setup for Apache, nginx, etc. that
properly creates a protected url that allows sendfile type requests.

The object allows flexible settings of virtually every kwarg at any point. If
you need to set the ``sendfile_url`` or ``doc_root`` dynamically, either when you
instantiate the box or when you call ``Giftbox.send()``, you can do that.

Tests
-----

All tests can be run using ``tox`` or ``python setup.py pytest``. A sample
``testettings.py`` is included in the package for Django compatibility.
