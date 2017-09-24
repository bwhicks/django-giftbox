==============
django-giftbox
==============


Description
-----------

django-giftbox is an app for the Django web framework that provides an easy
wrapper for xsendfile / x-accel-http functionality in Apache / lighthttp /
nginx. This lets users protect files by not allowing them to be downloaded
directly, but allows Django to programmatically send a redirect and let the
webserver handle the transaction.

Eventually this package will also provide some pre-slugged views for use with
a protected file setup.

The current implementation is compatible with Django 1.8+ (tested against LTS
releases) and py2/3 compatible. The only depedency is Django itself.

Installation
------------

Eventually this will be released to pypi. Until such time, however, you can
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

You can also specify these at run time, but you should at least have ``GIFTBOX_SETTINGS``
with some sane defaults defaults.

Usage
-----

In a view or view function, create an instance as follows::

  from gitfbox import GiftBox
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

Tests
-----

All tests can be run using ``tox`` or ``python setup.py pytest``. A sample
``testettings.py`` is included in the package for Django compatibility.
