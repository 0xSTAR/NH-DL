import os
import math
import httpx
import asyncio
import threading
from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import (
    Enum,
    unique,
    auto
)

from lang_db import (
    SELECTED_LANG,
    LANGS,
    LANG_DB
)

from PyQt6.QtCore import QThread, pyqtSignal

@unique
class NH_ENUMS(Enum):
    BASE_LNK = "https://nhentai.net/g/"
    SUPER_BASED_LNK = "https://nhentai.net"

    CONFIG = "nh.ini"

class Client(httpx.AsyncClient):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #self.headers.update(
        #    {
        #        "User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
        #        "Connection":"Keep-Alive"
        #    }
        #)

    @staticmethod
    def create_client() -> object:
        headers = {"user-agent":"Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0"}
        client = Client(
            headers=headers
        )
        return client

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
    increment:float=0.0
    text:str="Idling..."

@dataclass(frozen=True)
class valid_page:
    lnk:str
    filename:str

async def sift(PROG_BAR: Progress, code: str) -> valid_page:
    BASE_NHENTAI_LINK = NH_ENUMS.BASE_LNK.value
    SUPER_BASED_NHENTAI_LINK = NH_ENUMS.SUPER_BASED_LNK.value
    PROG_BAR.text = LANG_DB[SELECTED_LANG][3]

    async with Client.create_client() as _client:

        r0 = await _client.get(BASE_NHENTAI_LINK+code)
        soupy = BeautifulSoup(
            r0.text,
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
            PROG_BAR.increment:int = 100 / len(LAYER0_LINKS)
        except ZeroDivisionError:
            PROG_BAR.text:str = LANG_DB[SELECTED_LANG][8] + " 404"
            PROG_BAR.increment:int = 100

        # second layer and finally to then yield the pages
        for l0_lnk in LAYER0_LINKS:
            r1 = await _client.get(l0_lnk)
            soupy2 = BeautifulSoup(
                r1.text,
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
                    src_spl[3] == "jpg" or src_spl[3] == "png" or src_spl[3] == "jpeg"
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


async def download(client: Client, link:str, file_dest:str, _folder) -> None:
    print(_folder+file_dest)
    async with client as c:
        with open(_folder+file_dest,'wb') as dest:
            async with c.stream("GET", link) as stream_obj:
                async for chnk in stream_obj.aiter_bytes(chunk_size=4096):
                    dest.write(chnk)


class NHentai(QThread):
    progress_plus_txt_Signal = pyqtSignal(float, str)
    def __init__(self, code:str, savedir:str):

        super().__init__()
        self.__code:str = str(code)
        self.__folder = "{}/{}/".format(
            str(savedir), self.__code
        )
        self.progressBar = Progress()
        self.client = Client.create_client()

    def ptEmit(self) -> None:
        self.progress_plus_txt_Signal.emit(
            self.progressBar.percent,
            self.progressBar.text
        )

    def run(self) -> str:
        try:
            os.mkdir(path=str(self.__folder), mode=511, dir_fd=None)
        except FileExistsError:
            pass

        #os.chdir(self.__folder)

        ### TEST FOR CLOUDFLARE
        self.progressBar.text = "CHECKING FOR CLOUDFLARE..."
        self.ptEmit()
        test = httpx.get(
            NH_ENUMS.BASE_LNK.value + self.__code
        ).headers
        try:
            if test["server"] == "cloudflare":
                self.progressBar.text = "CLOUDFLARE DETECTED"
                self.ptEmit()
                #await self.client.aclose()
                asyncio.run(self.client.aclose())
                return
        except:
            pass
        self.progressBar.text = "NO CLOUDFLARE DETECTED"
        self.ptEmit()

        ###

        self.progressBar.text = LANG_DB[SELECTED_LANG][3]

        self.ptEmit()

        asyncio.run(self.run_async())

    async def run_async(self):
        async for lnk in sift(self.progressBar, self.__code):
            self.progressBar.text = LANG_DB[SELECTED_LANG][4]

            x = await download(self.client, lnk.lnk, lnk.filename, self.__folder)

            self.progressBar.percent += self.progressBar.increment
            self.progressBar.percent = 100 if (self.progressBar.percent > 100) else (
                    self.progressBar.percent
                )

                #self.progressBar.percent = math.floor(self.progressBar.percent)
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

        await self.client.aclose()
