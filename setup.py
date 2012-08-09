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

setup(
    name='django-content_blocks',
    version='3.0.0',
    description='Template tags for editable content block areas.',
    long_description=__doc__,
    packages=['content_blocks', 'content_blocks.templatetags'],
    include_package_data=True,
    install_requires=['django >= 1.3', 'django-linguo', 'markdown'],
    zip_safe=False,
    platforms='any',
    license='LICENSE',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
