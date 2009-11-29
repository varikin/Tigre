"""
Recursively sync a file directory to S3
"""
from collections import defaultdict
from datetime import datetime
import hashlib
from optparse import OptionParser
import os
from os.path import join

from boto.s3.connection import S3Connection
from boto.s3.key import Key

try:
    import simplejson as json
except ImportError:
    import json

class Config(object):
    """Loads the configuration from the config file.
   
    Also parses the options from the commandline to augement the config file.
    """

    def __init__(self):
        self.parse_options()
        rc_file = os.path.expanduser(self.options.config_file)
        try:
            config = json.load(open(rc_file))
        except IOError:
            print "Failed to open the config file %s" % rc_file
            import sys
            sys.exit(1)
        except ValueError:
            print "The config file could not be parsed"
            import sys
            sys.exit(1)

        self.key_id = self.options.key or config['access_key_id']
        self.secret_key = self.options.secret or config['secret_access_key']
        self.sync = config['sync']

    def parse_options(self):
        parser = OptionParser()
        parser.add_option('-c', '--config-file', metavar='FILE', dest='config_file',
                default='~/.tigrerc', help='The configuration file to use')
        parser.add_option('-k', '--key', metavar='ACCESS_KEY_ID', dest='key',
                default=None, help='The access key id for the S3 account')
        parser.add_option('-s', '--secret', metavar='SECRET_ACCESS_KEY', dest='secret',
                default=None, help='The secret access key for the S3 account')
        parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                default=False, help='Enabled verbose output')
        options, args = parser.parse_args()
        self.options = options



class Tigre(object):
    """Syncronizes a directory to a bucket on S3."""

    def __init__(self, connection):
        self.conn = connection

    def _get_local_files(self, path):
        """Returns a dictionary of all the files under a path."""
        if not path:
            raise ValueError("No path specified")
        files = defaultdict(lambda: None)
        path_len = len(path) + 1
        for root, dirs, filenames in os.walk(path):
            for name in filenames:
                full_path = join(root, name)
                files[full_path[path_len:]] = compute_md5(full_path) 
        return files

    def _get_s3_files(self, bucket):
        if not bucket:
            raise ValueError("No bucket specified")

        files = defaultdict(lambda: None)
        for f in bucket.list():
            if f.name.endswith('$folder$'):
                continue
            files[f.name] = f
        return files

    def sync_folder(self, path, bucket):
        """Syncs a local directory with an S3 bucket.
     
        Currently does not delete files from S3 that are not in the local directory.

        path: The path to the directory to sync to S3
        bucket: The name of the bucket on S3
        """
        local_files = self._get_local_files(path)
        s3_files = self._get_s3_files(self.conn.get_bucket(bucket))
        for filename, hash in local_files.iteritems():
            s3_key = s3_files[filename]
            if s3_key is None:
                s3_key = Key(bucket)
                s3_key.key = filename
                s3_key.etag = '"!"'
            
            if s3_key.etag[1:-1] != hash[0]:
                s3_key.set_contents_from_filename(join(path, filename), md5=hash)

    def sync(self, folders):
        """Syncs a list of folders to their assicated buckets.
        
        folders: A list of 2-tuples in the form (folder, bucket)
        """
        if not folders:
            raise ValueError("No folders to sync given")
        for folder in folders:
            self.sync_folder(*folder)

def compute_md5(path, block_size=8192):
    f = open(path)
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return (md5.hexdigest(), md5.digest())

def do_it():
    config = Config()
    folders = [(s['folder'], s['bucket']) for s in config.sync]
    conn = S3Connection(config.key_id, config.secret_key)
    tigre = Tigre(conn)
    tigre.sync(folders)

if __name__ == '__main__':
    do_it()
