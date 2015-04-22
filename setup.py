#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Documentation
-------------

The full documentation is at http://cache-requests.readthedocs.org/en/latest/.
"""

import os
import sys
import re


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


_version_re = re.compile(r"(?<=^__version__ = \')[\w\.]+(?=\'$)", re.U | re.M)
with open('cache_requests/__init__.py', 'rb') as f:
    version = _version_re.search(f.read().decode('utf-8')).group()

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

# TODO: put package requirements here
requirements = ['redislite', 'requests']

# TODO: put package test requirements here
test_requirements = ['pytest', 'mock']

# @:off
setup(
    name='cache_requests',
    version=version,
    description="Persistent LRU caching of the requests library.",
    long_description=readme + '\n\n' + __doc__ + '\n\n' + history,
    author="Manu Phatak",
    author_email='bionikspoon@gmail.com',
    url='https://github.com/bionikspoon'
        '/cache_requests',
    packages=[
        'cache_requests',
    ],
    package_dir={'cache_requests':
                 'cache_requests'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    cmdclass={'test': PyTest},
    keywords='cache_requests cache requests redis redislite Manu Phatak',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
# @:on