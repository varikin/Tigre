#!/usr/bin/env python
"""
Recursively sync a file directory to S3

Put the file names in a dictionary.
- The key is the filename (with relative path)
- The value is the timestamp

Get a dictionary filled with the local file
Get a list of files on S3 (in a specific bucket) and put in dictionary

Loop through the local files:
    Get the S3 file info
    If not found, upload the local file
    If local file is newer than S3 file, upload the local file
    Remove the data from the local and S3 dictionary

Loop through the S3 dictionary
    Remove from S3 (no local file anymore)
"""
from collections import defaultdict
from datetime import datetime
import hashlib
import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

def md5(path, block_size=8192):
    f = open(path)
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return (md5.hexdigest(), md5.digest())

def get_local_files(path):
    """Returns a dictionary of all the files under a path."""
    if not path:
        raise ValueError("No path specified")

    files = defaultdict(lambda: None)
    join = os.path.join
    stat = os.stat
    path_len = len(path) + 1
    for root, dirs, filenames in os.walk(path):
        for name in filenames:
            full_path = join(root, name)
            files[full_path[path_len:]] = md5(full_path) 
    return files

def get_s3_files(bucket):
    if not bucket:
        raise ValueError("No bucket specified")

    files = defaultdict(lambda: None)
    for file in bucket.list():
        if file.name.endswith('$folder$'):
            continue
        files[file.name] = file
    return files

def update_s3(local_files, s3_files, folder):
    join = os.path.join
    for filename, hash in local_files.iteritems():
        s3_key = s3_files[filename]
        if s3_key is None or s3_key.etag[1:-1] != hash[0]:
            s3_key.set_contents_from_filename(join(folder, filename), md5=hash)
            print "Updated %s" % filename
        
if __name__ == '__main__':
    key_id = '1NHPA19WDCS29ABACF82'
    secret = 'IGUn6kKBN3zUeZPo/JuyWQDa0W1FxMkU400CrKZ/'
    conn = S3Connection(key_id, secret)
    bucket = conn.get_bucket('nerdgames')
    s3_files = get_s3_files(bucket)
    local_files = get_local_files('/Users/varikin/code/nerdgames')
    updated_files = update_s3(local_files, s3_files, '/Users/varikin/code/nerdgames')


    

