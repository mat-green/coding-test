#  -*- coding: utf-8 -*-
"""
Setup tools script for tails.com postcodes application.
"""

import os

from setuptools import setup, find_packages

def required(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().split('\n')

config = {
    "name" : "postcodes",
    "version" : "19.03.0",
    "namespace_packages" : [ ],
    "packages" : find_packages(exclude=[
                                         "*.tests", "*.tests.*", "tests.*", "tests",
                                         "*.ez_setup", "*.ez_setup.*", "ez_setup.*", "ez_setup",
                                         "*.examples", "*.examples.*", "examples.*", "examples",
                                       ]),
    "include_package_data" : True,
    "package_data" : {
                       "" : [ ],
                     },
    "data_files" : [],
    "scripts" : [ ],
    "entry_points" : { },
    "install_requires" : [  required('requirements.txt') ],
    "tests_require" : [ required('requirements-for-test.txt') ],
    "test_suite" : 'pytest',
    "zip_safe" : False,

    # Metadata for upload to PyPI
    "author" : 'Matthew Green',
    "author_email" : "matthew@newedgeengineering.com",
    "description" : "Flask application that provides information about stores related to postcodes.",
    "long_description" : """This Flask application renders all stores and provides a lookup for neighbouring stores to a postcode for a give radius""",
    "classifiers" : [
                        'Environment :: Web Environment',
                        'Programming Language :: Python',
                    ],
    "license" : "",
    "keywords" : "",
    "url" : "",
}

setup(**config)
