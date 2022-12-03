#!/usr/bin/env python3
"""Make an Audio CD-R image from media files."""
from appdirs import *
from argparse import ArgumentParser
import os
from mkaudiocdrimg import mkimg
from os import getcwd, listdir, makedirs, umask
from os.path import abspath, basename, exists, isdir
from os.path import join as path_join
from pathlib import Path
import subprocess
from subprocess import run as sh

app_details = ("soundscope-player", "Pellegrino Prevete")
dirs = {'data': user_data_dir(*app_details),
        'config': user_config_dir(*app_details),
        'cache': user_cache_dir(*app_details)}

def err(msg):
    print_err(msg)
    exit()

def zenity_err(msg):
    zenity_cmd = ["zenity", "--icon=input-gaming", f"--error={msg}"]
    sh(zenity_cmd)

def check_requirements():
    if which("zenity"):
        print_err = zenity_error
    else:
        print_err = print
    programs = ['duckstation-nogui']
    for p in programs:
        if not which(p):
            err(f"This program needs '{p}' to work. Please install it.")

    ds_dirs = (path_join(user_data_dir("duckstation", "Connor McLaughlin"),
                                       "bios"),
               "/usr/share/psx")
    if not any("ps-41e.bin" in listdir(d) for d in ds_dirs):
        err("No SoundScope-enabled PlayStation bios found. Install `psx-bios` from AUR.")


def set_dirs(tmp_dir=dirs['cache']):
    original_umask = umask(0)
    path = path_join(tmp_dir, "convert")
    for d in dirs:
        try:
            makedirs(dirs[d], 0o700, exist_ok=True)
        except OSError:
            pass
    umask(original_umask)

def play(*media_src):
    set_dirs()
    mkimg(*media_src,
          out_dir=dirs['cache'],
          image_name="playback")
    ds_cmd = ["duckstation-nogui", "-settings"]
    sh(ds_cmd)

def main():
    check_requirements()
    parser_args = {"description": "PlayStation SoundScope player"}
    parser = ArgumentParser(**parser_args)

    media_source = {'args': ['media_source'],
                    'kwargs': {'nargs': '+',
                               'action': 'store',
                               'help': ("media source; "
                                        "default: current directory")}}

    parser.add_argument(*media_source['args'],
                        **media_source['kwargs'])

    args = parser.parse_args()

    play(*args.media_source) 

if __name__ == "__main__":
    main()
