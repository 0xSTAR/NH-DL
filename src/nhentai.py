import os
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import threading
import math

from PyQt6.QtCore import QThread, pyqtSignal

@dataclass
class valid_page:
    lnk:str
    filename:str

def sift(session, PROG_BAR, code:str) -> valid_page:
    BASE_NHENTAI_LINK = "https://nhentai.net/g/"
    SUPER_BASED_NHENTAI_LINK = "https://nhentai.net"

    PROG_BAR.text = "Fetching..."

    soupy = BeautifulSoup(
        session.get(BASE_NHENTAI_LINK + code).text,
        'html.parser'
    )

    LAYER0_LINKS:list = []

    #/g/337171/51/

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

    # set number of pages and use for
    # setting the increment value to the length of
    # the list of valid first layer pages
    try:
        PROG_BAR.increment:int = math.ceil( 100 / len(LAYER0_LINKS) )
    except ZeroDivisionError:
        #yield "ERROR 404"
        #return 
        PROG_BAR.text:str = "ERROR 404"
        PROG_BAR.increment:int = 100

    #print(LAYER0_LINKS)

    

    # second layer and finally to then yield the pages
    layer1_startswith:str = "https://i.nhentai.net/galleries/"
    for l0_lnk in LAYER0_LINKS:
        soupy2 = BeautifulSoup(
            session.get(l0_lnk).text,
            "html.parser"
        )
        for i,img in enumerate(soupy2.find_all('img'),start=1):
            src = img.get('src')
            if (
                src != None and 
                src.startswith(layer1_startswith)
            ):
                yield valid_page(
                    src,
                    src.split("/")[5]
                )
    del(layer1_startswith)
    del(soupy2)

    del(LAYER0_LINKS)

    del(BASE_NHENTAI_LINK)
    del(SUPER_BASED_NHENTAI_LINK)


def download(session, link:str, file_dest:str) -> None:
    with open(file_dest,'wb') as dest:
        for chnk in session.get(link,stream=True).iter_content(chunk_size=4096):
            dest.write(chnk)

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

        self.progressBar.text = "Fetching..."

        self.progress_plus_txt_Signal.emit(
            self.progressBar.percent,
            self.progressBar.text
        )

        for lnk in sift(self.session, self.progressBar, self.__code):
            self.progressBar.text = "Downloading..."

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

        self.progressBar.text = "Finished!"
        self.progressBar.percent = 100

        self.progress_plus_txt_Signal.emit(
            self.progressBar.percent,
            self.progressBar.text
        )
