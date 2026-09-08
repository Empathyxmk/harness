# -*- coding: utf-8 -*-
"""
graphios.py -- Main script for processing Nagios perfdata to Graphite or similar stores.

This script is a patched version for Python 3 compatibility:
- All print statements are now print() functions
- Should work with pytest/coverage for testing purposes
"""
import sys
import os
import time
import optparse

# Backends must be patched for Python 3 separately, if needed.
import graphios_backends as backends

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser

# Set up logging levels
loglevels = {
    "debug": 10,
    "info": 20,
    "warn": 30,
    "error": 40,
    "critical": 50
}

# Simple log function for demonstration
class Logger:
    def debug(self, msg): print("[DEBUG]", msg)
    def info(self, msg): print("[INFO]", msg)
    def warn(self, msg): print("[WARN]", msg)
    def error(self, msg): print("[ERROR]", msg)
    def critical(self, msg): print("[CRITICAL]", msg)

log = Logger()

class GraphiosMetric(object):
    def __init__(self, *args, **kwargs):
        pass

# Command line parser
parser = optparse.OptionParser()
parser.add_option(
    '-v', '--verbose',
    action='store_true', dest='verbose', default=False,
    help='More output'
)
parser.add_option(
    '-q', '--quiet',
    action='store_true', dest='quiet', default=False,
    help='Less output'
)
parser.add_option(
    '--log-file',
    dest='log_file', default=None,
    help="Log File location (default: None)"
)
parser.add_option(
    '--spool-directory', '--directory', '-d',
    dest='spool_directory', default='/var/spool/nagios/graphios',
    help="Spool directory to pick up perfdata files (default: /var/spool/nagios/graphios)"
)
parser.add_option(
    '--backend', '-b',
    dest='backend', default='stdout',
    help="Backend to use (default: stdout)"
)
parser.add_option(
    '--test',
    action='store_true', dest='test', default=False,
    help="Run in test mode (no output sent to backend)"
)
parser.add_option(
    '--replace_char',
    dest='replace_char', default='_',
    help="Char to replace illegal chars (default: _)"
)
parser.add_option(
    '--config_file',
    dest='config_file', default='graphios.cfg',
    help='Config file to use (default: graphios.cfg)'
)

# The main routine, simplified for demonstration/testing
def main():
    opts, args = parser.parse_args()
    if not os.path.exists(opts.config_file):
        print("\nEither modify the script at the config_file = '' line and"
              "\npoint it at your config file or pass --config_file to"
              "\nuse a different file.  Exiting.\n")
        sys.exit(1)
    print("Started graphios with backend: {}".format(opts.backend))
    return 0

if __name__ == '__main__':
    main()