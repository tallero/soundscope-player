#!/usr/bin/env python3
"""SoundScope PlayStation media player."""

#    soundscope-player
#
#    ----------------------------------------------------------------------
#    Copyright © 2022  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from appdirs import *
from argparse import ArgumentParser
import os
from mkaudiocdrimg import mkimg
from gi import require_version
require_version("Gtk", '3.0')
from gi.repository import Gtk
import glob
from os import getcwd, listdir, makedirs, umask
from os.path import abspath, basename, exists, dirname, isdir, realpath
from os.path import join as path_join
from pathlib import Path
from shutil import which
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
        print_err = zenity_err
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

def clean_cache():
    files = glob.glob(f"{dirs['cache']}/*")
    for f in files:
        print(f)

def fiximg(cue):
    with open(cue, "r") as handle:
        text = handle.read()
    with open(cue, "w") as handle:
        handle.write(text.replace("WAVE", "BINARY"))

def play(*media_src):
    ds_settings = path_join(dirname(realpath(__file__)), "settings.ini")
    set_dirs()
    mkimg(*media_src,
          out_dir=dirs['cache'],
          image_name="playback")
    cue = path_join(dirs['cache'], "playback.cue")
    fiximg(cue)
    ds_cmd = ["duckstation-nogui", "-settings", ds_settings, cue]
    sh(ds_cmd)
    clean_cache()

def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    media_prompt = Gtk.FileChooserDialog(title="Select media",
                                         parent=win,
                                         action=Gtk.FileChooserAction.SELECT_FOLDER) #OPEN)
    media_prompt.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
    media_prompt.set_select_multiple(True)
    response = media_prompt.run()
    if response  == Gtk.ResponseType.OK:
        app.filenames = media_prompt.get_filenames()
        print(f"File selected: {app.filename}")
    elif response == Gtk.ResponseType.CANCEL:
        print("Canceled")
    media_prompt.destroy()
    app.quit()
    # play(filename) 

def select_media():
    app = Gtk.Application(application_id="com.sony.SoundScopePlayer")
    app.connect("activate", on_activate)
    app.run(None)
    play(*app.filenames) 

def main():
    check_requirements()
    parser_args = {"description": "PlayStation SoundScope player"}
    parser = ArgumentParser(**parser_args)

    media_source = {'args': ['media_source'],
                    'kwargs': {'nargs': '?',
                               'action': 'store',
                               'help': ("media source; "
                                        "default: current directory")}}

    parser.add_argument(*media_source['args'],
                        **media_source['kwargs'])

    args = parser.parse_args()

    if not args.media_source:
        select_media()
    else:
        play(*args.media_source) 

if __name__ == "__main__":
    main()
