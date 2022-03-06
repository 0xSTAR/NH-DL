import os
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import threading
import math

from lang_db import (
    SELECTED_LANG,
    LANGS,
    LANG_DB
)

from PyQt6.QtCore import QThread, pyqtSignal

class Session(requests.Session):
    def __init__(self):
        super().__init__()

        self.headers.update(
            {
                "User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
                "Connection":"Keep-Alive"
            }
        )

class Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __start(self):
        self.start()

    def __join(self):
        self.join()

@dataclass
class Progress:
    percent:float=0.0
    increment:int=0
    text:str="Idling..."

@dataclass
class valid_page:
    lnk:str
    filename:str

def sift(session:Session, PROG_BAR:Progress, code:str) -> valid_page:
    BASE_NHENTAI_LINK = "https://nhentai.net/g/"
    SUPER_BASED_NHENTAI_LINK = "https://nhentai.net"

    PROG_BAR.text = LANG_DB[SELECTED_LANG][3]

    soupy = BeautifulSoup(
        session.get(BASE_NHENTAI_LINK + code).text,
        'html.parser'
    )

    LAYER0_LINKS:list = []

    # get the first layer of pages
    layer0_startswith:str = "/g/{}/".format(
        code
    )
    for a in soupy.find_all('a'):
        href = a.get('href')
        if (
            href != None and 
            href.startswith(layer0_startswith) and 
            not (SUPER_BASED_NHENTAI_LINK + href) in LAYER0_LINKS
        ):
            LAYER0_LINKS.append(SUPER_BASED_NHENTAI_LINK + href)
        del(href) 
    del(layer0_startswith)

    del(soupy)

    try:
        PROG_BAR.increment:int = math.ceil( 100 / len(LAYER0_LINKS) )
    except ZeroDivisionError:
        PROG_BAR.text:str = LANG_DB[SELECTED_LANG][8] + " 404"
        PROG_BAR.increment:int = 100

    # second layer and finally to then yield the pages
    for l0_lnk in LAYER0_LINKS:
        soupy2 = BeautifulSoup(
            session.get(l0_lnk).text,
            "html.parser"
        )
        for i,img in enumerate(soupy2.find_all('img'),start=1):
            src = img.get('src')
            src_spl = src.split('.')
            if (
                src != None and 
                src_spl[0].startswith("https://i") and
                src_spl[1] == "nhentai" and
                src_spl[2].startswith("net/galleries/") and
                src_spl[3] == "jpg"
            ):
                yield valid_page(
                    src,
                    src.split("/")[5]
                )
            del(src)
            del(src_spl)

        del(soupy2)

    del(LAYER0_LINKS)

    del(BASE_NHENTAI_LINK)
    del(SUPER_BASED_NHENTAI_LINK)


def download(session:Session, link:str, file_dest:str) -> None:
    with open(file_dest,'wb') as dest:
        for chnk in session.get(link,stream=True).iter_content(chunk_size=4096):
            dest.write(chnk)


class NHentai(QThread):
    progress_plus_txt_Signal = pyqtSignal(int, str)
    def __init__(self, code:str, savedir:str, session:Session):
        super().__init__()
        self.__code:str = str(code)
        self.__folder = "{}/{}/".format(
            str(savedir), self.__code
        )
        self.progressBar = Progress()

        self.session = session

    def run(self) -> str:
        try:
            os.mkdir(path=str(self.__folder), mode=511, dir_fd=None)
        except FileExistsError:
            pass

        os.chdir(self.__folder)

        self.progressBar.text = LANG_DB[SELECTED_LANG][3]

        self.progress_plus_txt_Signal.emit(
            self.progressBar.percent,
            self.progressBar.text
        )

        for lnk in sift(self.session, self.progressBar, self.__code):
            self.progressBar.text = LANG_DB[SELECTED_LANG][4]

            download(self.session, lnk.lnk, lnk.filename)

            self.progressBar.percent += self.progressBar.increment

            self.progressBar.percent = 100 if (self.progressBar.percent > 100) else (
                self.progressBar.percent
            )

            self.progressBar.percent = math.floor(self.progressBar.percent)

            self.progress_plus_txt_Signal.emit(
                self.progressBar.percent,
                self.progressBar.text
            )

        self.progressBar.text = LANG_DB[SELECTED_LANG][5]
        self.progressBar.percent = 100

        self.progress_plus_txt_Signal.emit(
            self.progressBar.percent,
            self.progressBar.text
        )
