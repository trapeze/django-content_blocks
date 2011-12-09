#!/usr/bin/env python
"""
Content Blocks
--------------

This application provides a model and the necessary template tags for defining
editable content block areas in the templates. Without any need for initial
data, it can generate the blocks in the database when required. It also
provides an "Edit" link next to the blocks. If JavaScript is enabled and the
included JS class is loaded, these links enable AJAX-based, inline editing
of content right in the page. Otherwise, they become simple links to the admin
area of the selected block.

See README for more details.
"""
from setuptools import setup
import os

__version__ = file(os.path.join(os.path.dirname(__file__), 'RELEASES')).readline().strip().split('-')[1]

# setup(name=_name, version=_version, packages=[_name])

setup(
    name='content_blocks',
    version=__version__,
    description='Template tags for editable content block areas.',
    long_description=__doc__,
    packages=['content_blocks', 'content_blocks.templatetags'],
    include_package_data=True,
    install_requires=['django >= 1.3', 'django-linguo', 'markdown'],
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
