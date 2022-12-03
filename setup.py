#!/usr/bin/env python3
"""Setup for SoundScope player"""
from platform import system, machine
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="SoundScope Player",
    version="1.0",
    author="Pellegrino Prevete",
    author_email="pellegrinoprevete@gmail.com",
    description="SoundScope PlayStation media player",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tallero/soundscope-player",
    packages=find_packages(),
    package_data={
        '': ['settings.ini'],
    },
    entry_points={
        'console_scripts': ['soundscope-player = soundscope:main']
    },
    install_requires=[
        'appdirs',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Unix",
    ],
)
