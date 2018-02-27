#!/usr/bin/env python3

import os
import sys

from setuptools import find_packages, setup

import e_ood_django

VERSION = e_ood_django.__version__

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

setup(
    name='emptyhammock-out-of-date-django',
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0 License',
    version=VERSION,
    description='A Django app for maintaining a package release database for use with emptyhammock-out-of-date',
    author='Emptyhammock Software and Services LLC',
    author_email='info@emptyhammock.com',
    url='https://github.com/trawick/emptyhammock-out-of-date-django',
    keywords=['django', 'pypi'],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
    ],
)
