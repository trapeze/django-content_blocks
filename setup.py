import os

from distutils.core import setup


_name, _version = file(os.path.join(os.path.dirname(__file__), 'RELEASES')).readline().strip().split('-')


setup(name=_name, version=_version, packages=[_name])
