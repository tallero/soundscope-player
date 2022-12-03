#!/usr/bin/env python3
"""Setup for SoundScope player"""
from pathlib import Path
from platform import system, machine
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

data_files = []

# Variables
theme_dir = "data/icons/hicolor"
hicolor_path = "share/icons/hicolor"

# Auxiliary functions
# for paths
in_hicolor_src = lambda x: join(theme_dir, x)
in_hicolor = lambda x: join(hicolor_path, x)

# to install data files
encode = lambda src, dest: (dest, [src])
add_data_file = lambda src, dest: data_files.append(encode(src, dest))

# to install icons
def encode_icon(icon):
    icon_path = str(Path(icon).parents[0])
    return encode(in_hicolor_src(icon), in_hicolor(icon_path))
add_icon = lambda icon: data_files.append(encode_icon(icon))

add_data_file('data/com.sony.SoundScopePlayer.desktop', 'share/applications')

icons = ['scalable/apps/com.sony.SoundScopePlayer.svg',]

for icon in icons:
    add_icon(icon)

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
    data_files = data_files,
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
