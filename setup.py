"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Credit to Kenneth Reitz's remarkably sane
# https://github.com/kennethreitz/setup.py

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(path.join(here, 'giftbox', 'version.py')) as f:
    exec(f.read(), about)


TESTS_REQUIRE = ['pytest', 'pytest-django', 'pytest-cov',
                 'mock', 'python-magic', 'tox', 'tox-travis']


setup(
    name='django-giftbox',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=about['__version__'],

    description='A package that includes xsendfile capabilities for Django',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/bwhicks/django-giftbox',

    # Author details
    author='Benjamin Hicks',
    author_email='benajmin.w.hicks@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 1.8',
    ],

    # What does your project relate to?
    keywords='sendfile, apache',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    setup_requires=['pytest-runner'],
    tests_require=TESTS_REQUIRE,
    install_requires=['django>=1.8'],
    extras_require={
        'magic': ['python-magic'],
        'test': TESTS_REQUIRE,
        'develop': TESTS_REQUIRE + ['twine']
    },

)
