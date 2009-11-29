Tigre
=====

Tigre syncs directories to buckets on S3. It is named for the Tigre river that
feeds into the Amazon River.

Installation
------------

Run `python setup.py install` to install the `tigre` script. Or just copy the
`tigre` file to where every you wish.

Configuration
-------------

Tigre uses a configuration file, ~/.tigre.rc. A different file can be specified
by `tigre -c somefile`. The configuration file is in the JSON format. See
`tigre.rc.sample` for a sample configuration file.
