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
import os
import boto

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
            full = join(root, name)
            mtime = stat(full).st_mtime
            files[full[path_len:]] = datetime.fromtimestamp(mtime)
    return files

def get_s3_files(bucket):
    files = defaultdict(lambda: None)
    for file in bucket.list():
        if file.name.endswith('$folder$'):
            continue
        files[file.name] = datetime.strptime(file.last_modified, "%Y-%m-%dT%H:%M:%S.000Z")
    
    return files

def get_new_files(local_files, s3_files):
    new_files = []
    for name, modified in local_files.iteritems():
        uploaded = s3_files[name]
        if uploaded is None or uploaded < modified:
            new_files.append(name)
        del s3_files[name]
    return new_files

if __name__ == '__main__':
    key_id = '1NHPA19WDCS29ABACF82'
    secret = 'IGUn6kKBN3zUeZPo/JuyWQDa0W1FxMkU400CrKZ/'
    conn = boto.connect_s3(key_id, secret)
    bucket = conn.get_bucket('nerdgames')
    s3_files = get_s3_files(bucket)
    local_files = get_local_files('/Users/varikin/code/nerdgames')
    print s3_files
    print "\n\n"
    print local_files
    print "\n\n"
    updated_files = get_new_files(local_files, s3_files)
    print updated_files

    

