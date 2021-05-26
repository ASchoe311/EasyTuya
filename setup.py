#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='EasyTuya',
    version='0.1.371',
    description='Interact with devices connected to the Tuya IOT platform through Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Adam Schoenfeld',
    author_email='aschoe@umich.edu',
    python_requires='>=3.6.0',
    project_urls={
        'Documentation': 'https://aschoe311.github.io/EasyTuya/',
        'Source': 'https://github.com/ASchoe311/EasyTuya'
    },
    keywords='tuya iot tuyaapi smartlights',
    packages=['EasyTuya', 'EasyTuya.devices'],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=[
        'pycryptodome'
    ],
    include_package_data=True,
    license='GNU GPLv3',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
		'Development Status :: 1 - Planning'
    ]
)