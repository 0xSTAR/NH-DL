#!/usr/bin/env python3

# GUI / CLI

import sys
import os
from base_ui import Ui_Form as Base_Ui
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

import nhentai
import startup
import cli
from lang_db import (
    SELECTED_LANG,
    LANGS,
    LANG_DB
)

import platform
from typing import NoReturn
from tkinter import Tk
from tkinter.filedialog import askdirectory

INSTALLED = True if (
    sys.platform == 'win32' and os.path.isdir("C:/Program Files/nh-dl/")
) else (
    True
) if (
    (sys.platform == 'darwin' or sys.platform == 'linux') and os.path.isdir('~/nh-dl/')
) else False

STANDALONE = not INSTALLED

class NH(QtWidgets.QWidget, Base_Ui):
    def __init__(self):
        super().__init__()

        super().setupUi(self)

        self.setWindowTitle("NH")

        if INSTALLED:
            ico = QIcon("C:/Program Files/nh-dl/content/nh.png") if (
                    self.PLATFORM == "Windows" and os.path.isfile("C:/Program Files/nh-dl/content/nh.png")
                ) else QIcon("~/nh-dl/content/nh.png") if (
                    (self.PLATFORM == 'Linux' or self.PLATFORM == 'Darwin') and os.path.isfile("~/nh-dl/content/nh.png")
                ) else None

        elif STANDALONE:
            ico = QIcon("content/nh.png")

        self.setWindowIcon(ico) if (ico != None) else None
        del(ico)

        # DL BUTTON is exitButton_2
        self.exitButton_2.clicked.connect(self.dl)
        #self.exitButton.clicked.connect(self.EXIT)
        self.changeDirectory.clicked.connect(self.changeSaveDir)

    def FRAMELESS(self) -> None:
        # for the legacy transparent UI
        self.setWindowFlags(
                QtCore.Qt.WindowType(0x00000800)
        )
        self.setAttribute(
                QtCore.Qt.WidgetAttribute(0x78) # (int: 120)
                # QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )

    def initialize(self) -> None:

        self.DOWNLOADING = False

        self.nh_instance = None
        self.nh_thread = None
        self.nh_progress_thread = None

        self.EXPLORER = Tk()
        self.EXPLORER.withdraw() # make sure not showing in unnecessary situations

        #self.PLATFORM = sys.platform
        self.PLATFORM = platform.system()
        self.session = nhentai.Session()

        # get path for executable for default
        self.EXE_PATH = __file__
        self.EXE_FOLDER = (
            self.EXE_PATH.split("\\") if self.PLATFORM == 'Windows' else
            self.EXE_PATH.split('/') if self.PLATFORM == 'Linux' or self.PLATFORM == 'Darwin' else
            self.EXE_PATH.split('/')
        )

        del(self.EXE_FOLDER[-1])

        tmp_path:str = ""

        for i in self.EXE_FOLDER:
            tmp_path+= (i + "/")

        self.EXE_FOLDER = tmp_path
        del(tmp_path)

        # default value
        self.saveToDirectory = (
            "C:/Users/" + self.EXE_FOLDER.split('/')[2] + "/Downloads/" if self.PLATFORM == 'Windows' and
            os.path.isdir("C:/Users/" + self.EXE_FOLDER.split('/')[2] + "/Downloads/")  else
            "~/Downloads/" if self.PLATFORM == 'Linux' or self.PLATFORM == 'Darwin' else
            None
        )

        self.saveDirectory.setText("..." + self.saveToDirectory[-22:]) if self.saveToDirectory != None else (
            self.saveDirectory.setPlaceholderText('Select a Directory')
        )

        # persistency (to be added in future)
        if INSTALLED:
            config_present = True if (
                self.PLATFORM == 'Windows' and os.path.isfile("C:/Program Files/nh-dl/conf.ini")
            ) else True if (
                (self.PLATFORM == 'Linux' or self.PLATFORM == 'Darwin') and os.path.isfile("~/nh-dl/conf.ini")
            ) else False

            if config_present:
                print("Config file present.")
            else:
                print("ERROR: Config file not present")


        elif STANDALONE:
            pass

        return

    def EXIT(self) -> NoReturn:
        print("EXITING...")
        sys.exit()

    def isInt(self, x) -> bool:
        try:
            type(int(x))
        except ValueError:
            return False
        return True

    def isOk(self,saucy:str) -> bool:
        for i in saucy:
            if not self.isInt(i):
                return False
        return True

    def dl(self) -> None:
        # all numbers are
        # in between 0-9, then run the download
        sauceCode:str = self.sauceBox.text()

        if (
            self.isOk(sauceCode) and
            not self.DOWNLOADING
        ):
            self.DOWNLOADING = True

            print("Instantiating extractor worker thread...")
            self.nh_instance = nhentai.NHentai(sauceCode, self.saveToDirectory, self.session)

            print("Beginning Download...")
            self.nh_instance.start()
            self.nh_instance.finished.connect(self.finishDL)
            self.nh_instance.progress_plus_txt_Signal.connect(self.progress_N_txt)


        del(sauceCode)

    def finishDL(self) -> None:
        print("Extractor worker thread ended.")
        print("Destroying extractor worker instance...")
        del(self.nh_instance)
        print("Extractor worker instance destroyed")

        self.DOWNLOADING = False

    def progress_N_txt(self, x:float, y:str) -> None:
        self.progressionBar.setValue( int(x) )
        self.labelStatus.setText( y )

    def changeSaveDir(self) -> None:
        print("Opening file dialog...")
        filePrompt = askdirectory(mustexist=True)

        if filePrompt != '':
            print("Directory received.")
            self.saveToDirectory:str = str(filePrompt)
            self.saveDirectory.setText("..." + self.saveToDirectory[-22:])
        else:
            print("No directory received.")

        del(filePrompt)
        return

if __name__ == '__main__':
    # GUI
    if not len(sys.argv) > 1:
        nh_app = QtWidgets.QApplication([])

        nh_widget = NH()
        nh_widget.show()

        nh_widget.initialize()

        nh_app.exec()

    else:
        # CLI
        nh_cli = cli.NH_CLI(str(sys.argv[1]))
        nh_cli.run()
