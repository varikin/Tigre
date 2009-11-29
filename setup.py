import os
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "tigre",
    version = "0.1",
    author = "John Shimek",
    author_email = "varikin@gmail.com",
    description = ("Syncs directories to buckets on S3."),
    license = "Apache Software License 2.0",
    keywords = "backup S3 Amazon sync",
    url = "http://github.com/varikin/tigre",
    py_modules = ['tigre'],
    long_description = read('README'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Archiving :: Backup",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Programming Language :: Python",
    ],
    zip_ok = False,
) 
