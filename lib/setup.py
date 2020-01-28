'''
Template for setup.py that is symlinked in the indidivual packages
    located at the path `./lib/<package-name>`. This script dynamically
    generates values that are used in the setup.py script.
'''
import os
import sys
import time
from setuptools import setup, find_packages

# Full path to the symbolic link location (which points to setup.py)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FN = 'VERSION'  # Name of file with current version


def get_name() -> str:
    ''' Get package name from the directory name '''
    package_name = os.path.basename(PACKAGE_DIR)
    return package_name


def get_version() -> str:
    ''' Get version from the VERSION file in the directory '''
    with open(os.path.join(PACKAGE_DIR, VERSION_FN)) as version_file:
        version = version_file.read().strip()
    if version:
        version = version + 'rc' + str(int(time.time()))
        return version
    else:
        print('VERSION file was empty.')
        sys.exit(1)


NAME = get_name()
VERSION = get_version()


setup(
    name=NAME,
    version=VERSION,
    author='Jared Hanson',
    author_email='jred0011@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    data_files=[('', ['VERSION'])],
    setup_requires=['wheel']
)
