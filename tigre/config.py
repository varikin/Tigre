from optparse import OptionParser
import os

try:
    import simplejson as json
except ImportError:
    import json

class Config(object):
    """Loads the configuration from the config file.
   
    Also parses the options from the commandline to augement the config file.
    """

    def __init__(self):
        parse_options()
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
                default='~/.backup.rc', help='The configuration file to use')
        parser.add_option('-k', '--key', metavar='ACCESS_KEY_ID', dest='key',
                default=None, help='The access key id for the S3 account')
        parser.add_option('-s', '--secret', metavar='SECRET_ACCESS_KEY', dest='secret',
                default=None, help='The secret access key for the S3 account')
        parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                default=False, help='Enabled verbose output')
        options, args = parser.parse_args()
        self.options = options

