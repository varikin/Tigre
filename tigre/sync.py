#!/usr/bin/env python
"""
Recursively sync a file directory to S3
"""
from collections import defaultdict
from datetime import datetime
import hashlib
import os
from os.path import join

from boto.s3.connection import S3Connection
from boto.s3.key import Key

def _compute_md5(path, block_size=8192):
    f = open(path)
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return (md5.hexdigest(), md5.digest())

def _get_local_files(path):
    """Returns a dictionary of all the files under a path."""
    if not path:
        raise ValueError("No path specified")

    files = defaultdict(lambda: None)
    path_len = len(path) + 1
    for root, dirs, filenames in os.walk(path):
        for name in filenames:
            full_path = join(root, name)
            files[full_path[path_len:]] = _compute_md5(full_path) 
    return files

def _get_s3_files(bucket):
    if not bucket:
        raise ValueError("No bucket specified")

    files = defaultdict(lambda: None)
    for file in bucket.list():
        if file.name.endswith('$folder$'):
            continue
        files[file.name] = file
    return files

def sync_s3(path, bucket):
    """Syncs a local directory with an S3 bucket.
 
    Currently does not delete files from S3 that are not in the local directory.

    path: The path to the directory to sync to S3
    bucket: The name of the bucket on S3
    """
    local_files = _get_local_files(path)
    s3_files = _get_s3_files(bucket)
    for filename, hash in local_files.iteritems():
        s3_key = s3_files[filename]
        
        if s3_key is None:
            s3_key = Key(bucket)
            s3_key.key = filename
            s3_key.etag = '"!"'
        
        if s3_key.etag[1:-1] != hash[0]:
            s3_key.set_contents_from_filename(join(path, filename), md5=hash)

if __name__ == '__main__':
    config = Config()
    conn = S3Connection(config.key_id, config.secret_key)
    for sync in config.sync:
        sync_s3(sync['folder'], conn.get_bucket(sync['bucket']))
