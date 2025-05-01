#!/usr/bin/env python
import io

from setuptools import setup, find_packages
from wagtail_advanced_form_builder import __version__
# Hack to prevent "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when setup.py exits
# (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass

with io.open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wagtail-advanced-form-builder",
    version=__version__,
    description="Wagtail Advanced Form Builder",
    long_description=long_description,
    author="Richard Blake (Octave)",
    author_email="richard.blake@octave.nz",
    url="https://github.com/octavenz/wagtail-advanced-form-builder",
    packages=find_packages(exclude=("build_test",)),
    include_package_data=True,
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Wagtail :: 6"
    ],
    install_requires=[
        "Django>=4.2",
        "Wagtail>=6",
        "wagtailextraicons"
    ],
    extras_require={
        'headless':  [
            "django-recaptcha",
            "django-ninja",
            "celery"
        ]
    },
    zip_safe=False,
)
