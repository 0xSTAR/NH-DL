#!/usr/bin/env python3

"""

The bootstrapper is for Windows users to make an installer

"""

import sys
import os
import subprocess
import PyInstaller.__main__

import build_nh
import build_ins

subprocess.call(
    [
    sys.executable,
    '-m',
    'pip',
    'install',
    '-r',
    'requirements.txt'
    ]
)

cwd = os.getcwd()

srcDIR = "./src/"
insDIR = "./win_installer/"

build_nh.main()

"""class Bootstrapper(object):
    def __init__(self):
        self.cwd = os.getcwd()"""

os.chdir(insDIR)

subprocess.call(
    [
        sys.executable,
        'gen_data.py'
    ]
)
