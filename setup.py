import os
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

def requirements():
    """Returns the requirements for this package.

    If the `json` module can not be imported, then `simplejson` is needed.
    `Simplejson` was added to Python 2.6 as `json`.
    """
    requires = ['boto']
    try:
        import json
    except ImportError:
        requires.append('simplejson')
    return requires

def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "tigre",
    version = "0.1.6",
    author = "John Shimek",
    author_email = "varikin@gmail.com",
    description = ("Syncs directories to buckets on S3."),
    license = "Apache Software License 2.0",
    keywords = "backup S3 Amazon sync",
    url = "http://github.com/varikin/tigre",
    packages = ['tigre'],
    scripts = ['scripts/tigre'],
    long_description = read('README.rst'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Archiving :: Backup",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Programming Language :: Python",
    ],
    install_requires = requirements(),
    zip_safe = False,
) 
