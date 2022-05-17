#!/usr/bin/env python3

# GUI / CLI

import sys
import os
from base_ui import Ui_Form as Base_Ui
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

import nhentai
import startup
#import cli
from lang_db import (
    SELECTED_LANG,
    LANGS,
    LANG_DB
)

import platform
from typing import NoReturn
from tkinter import Tk
from tkinter.filedialog import askdirectory
import configparser

STANDALONE = True

class NH(QtWidgets.QWidget, Base_Ui):
    def __init__(self):
        super().__init__()

        super().setupUi(self)

        self.setWindowTitle("NH")

        if STANDALONE: ico = QIcon("content/nh.png")

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

        # save directory & persistency
        if STANDALONE and os.path.isfile(
            nhentai.NH_ENUMS.CONFIG.value
        ):
            conf = configparser.ConfigParser()
            conf.read(nhentai.NH_ENUMS.CONFIG.value)
            self.saveToDirectory = conf["NH"]["SAVE_DIR"]
            del conf
        else:
            self.saveToDirectory = os.getcwd()#.replace("\\","/")

        self.saveDirectory.setText("..." + self.saveToDirectory[-15:]) if self.saveToDirectory != None else (
            self.saveDirectory.setPlaceholderText('Select a Directory')
        )

        return

    def EXIT(self) -> NoReturn:
        print("EXITING...")

        with open(nhentai.NH_ENUMS.CONFIG.value, "w") as conf_file:

            conf = configparser.ConfigParser()
            conf["NH"] = {}
            conf["NH"]["SAVE_DIR"] = self.saveToDirectory
            conf.write(conf_file)

        sys.exit()

    @staticmethod
    def isInt(x) -> bool:
        try:
            type(int(x))
        except ValueError:
            return False
        return True

    @staticmethod
    def isOk(saucy:str) -> bool:
        for i in saucy:
            if not NH.isInt(i):
                return False
        return True

    def dl(self) -> None:
        # all numbers are
        # in between 0-9, then run the download
        sauceCode:str = self.sauceBox.text()

        if (
            NH.isOk(sauceCode) and
            not self.DOWNLOADING
        ):
            self.DOWNLOADING = True

            print("Instantiating extractor worker thread...")
            self.nh_instance = nhentai.NHentai(sauceCode, self.saveToDirectory)

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

        if filePrompt != '' and filePrompt != None and filePrompt != ():
            print("Directory received.")
            self.saveToDirectory:str = str(filePrompt)
            self.saveDirectory.setText("..." + self.saveToDirectory[-15:])
        else:
            print("No directory received.")

        del(filePrompt)
        return

if __name__ == '__main__':
    # GUI
    if not len(sys.argv) > 1:
        nh_app = QtWidgets.QApplication([])

        nh_widget = NH()

        nh_widget.initialize()
        nh_widget.show()

        nh_app.exec()
        nh_widget.EXIT()

    #else:
    #    # CLI
    #    nh_cli = cli.NH_CLI(str(sys.argv[1]))
    #    nh_cli.run()
