import sys
import os
import shutil
import configparser

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')
COVERAGE_FOLDER = config['DEFAULT']['coverage_folder']

trace_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(COVERAGE_FOLDER)))
if os.path.exists(trace_dir):
    shutil.rmtree(trace_dir)
