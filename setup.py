#!/usr/bin/env python

import sys, os

from setuptools import setup, find_packages

# Hack to prevent "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when setup.py exits
# (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name="wagtail-advanced-form-builder",
    version="0.1.0",
    description="Wagtail Advanced Form Builder",
    author="Richard Blake (Octave)",
    author_email="richard.blake@octave.nz",
    url="https://octave.nz",
    packages=find_packages(),
    include_package_data=True,
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=["Django>=2.2,<3.2", "Wagtail>=2.7,<2.11", "wagtailextraicons"],
    zip_safe=False,
)
