import os
import math
import httpx
import asyncio
import threading
from dataclasses import dataclass
import json

from lang_db import SELECTED_LANG, LANGS, LANG_DB

from PyQt6.QtCore import QThread, pyqtSignal

from nh_enums import NH_ENUMS

import LOAD_BREAK

async def WRAP_THE_BREAK(x: str) -> httpx.Cookies:
    return (await LOAD_BREAK.GET_BREAK_IT(x))

class Client(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_client(cls) -> object:
        #PRE_COOKIES: httpx.Cookies = asyncio.run(WRAP_THE_BREAK(LNK_TO_BRK))
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0"
        }
        client = cls(headers=headers)#,cookies=PRE_COOKIES)
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
    percent: float = 0.0
    increment: float = 0.0
    text: str = "Idling..."


@dataclass(frozen=True)
class valid_page:
    lnk: str
    filename: str


async def sift(_client: Client, PROG_BAR: Progress, code: str, BROKEN_JSON = None) -> valid_page:
    PROG_BAR.text = LANG_DB[SELECTED_LANG][3]

    api_lnk: str = NH_ENUMS.NH_API.value
    img_lnk: str = NH_ENUMS.IMG_URL.value

    # api scraper

    if BROKEN_JSON == None:
        r0 = await _client.get(api_lnk + code)
        j0 = r0.json()
    else:
        j0 = BROKEN_JSON

    EXTEND = {"j": ".JPG", "p": ".PNG", "g": ".GIF"}  # LOL, IT SPELLS OUT JPG

    dj_pages = j0["images"]["pages"]
    try:
        PROG_BAR.increment: int = 100 / len(dj_pages)
    except ZeroDivisionError:
        PROG_BAR.increment: int = 100
        PROG_BAR.text = LANG_DB[SELECTED_LANG][8] + " 404"

    TRUE_ID = str(int(j0["media_id"]))

    for no, p in enumerate(dj_pages, start=1):
        fn: str = "{}{}".format(str(no), EXTEND[p["t"]].lower())
        yield valid_page("{}{}/{}".format(img_lnk, TRUE_ID, fn), fn)

    # bye bye frontend scraper !


async def download(client: Client, link: str, file_dest: str, _folder) -> None:
    with open(_folder + file_dest, "wb") as dest:
        async with client.stream("GET", link) as stream_obj:
            async for chnk in stream_obj.aiter_bytes(chunk_size=4096):
                dest.write(chnk)


class NHentai(QThread):
    progress_plus_txt_Signal = pyqtSignal(float, str)

    def __init__(self, code: str, savedir: str):

        super().__init__()
        self.__code: str = str(code)
        self.__folder = "{}/{}/".format(str(savedir), self.__code)
        self.progressBar = Progress()

        
        #self.client = Client.create_client()

    def ptEmit(self) -> None:
        self.progress_plus_txt_Signal.emit(
            self.progressBar.percent, self.progressBar.text
        )

    def detectCloudFlare(self) -> None:
        self.progressBar.text = "CHECKING FOR CLOUDFLARE..."
        self.ptEmit()
        test = httpx.get(NH_ENUMS.NH_API.value + self.__code).headers
        try:
            if test["server"] == "cloudflare":
                self.progressBar.text = "CLOUDFLARE DETECTED"
                self.ptEmit()
            else:
                self.progressBar.text = "NO CLOUDFLARE DETECTED"
        except:
            pass

        self.ptEmit()

    def run(self) -> str:
        self.client = Client.create_client()

        try:
            os.mkdir(path=str(self.__folder), mode=511, dir_fd=None)
        except FileExistsError:
            pass

        # os.chdir(self.__folder)

        ### TEST FOR CLOUDFLARE
        # self.detectCloudFlare()

        ###

        self.progressBar.text = LANG_DB[SELECTED_LANG][3]

        self.ptEmit()

        asyncio.run(self.run_async())

    async def run_async(self):
        # RUN TEST #

        CLOUDFLARE_DETECTED: bool = False

        r0 = await self.client.get(NH_ENUMS.NH_API.value + self.__code, follow_redirects=True)
        #await asyncio.sleep(10)
        j0 = None
        try:
            j0 = r0.json()
        except json.decoder.JSONDecodeError:
            CLOUDFLARE_DETECTED = not CLOUDFLARE_DETECTED
            self.progressBar.text = "CloudFlare Detected"
            self.progressBar.percent = 0
            self.ptEmit()
            await asyncio.sleep(0.5)
            # THIS ONE NEEDS TO GET THE GODDAMN SWEETS

        del r0
        del j0

        ###############

        FEED_JSON = None
        BYPASS_WORK = True

        if CLOUDFLARE_DETECTED:
            self.progressBar.text = "Breaking CloudFlare..."
            self.ptEmit()

            try:
                FEED_JSON = await WRAP_THE_BREAK(NH_ENUMS.NH_API.value + self.__code)
            except:
                BYPASS_WORK = False
            #print(FEED_JSON)

        if (BYPASS_WORK == False):
            self.progressBar.text = "ERR: Bypass Failed"

        if not (BYPASS_WORK == False):
            async for lnk in sift(self.client, self.progressBar, self.__code,FEED_JSON):
                self.progressBar.text = LANG_DB[SELECTED_LANG][4]

                x = await download(self.client, lnk.lnk, lnk.filename, self.__folder)

                self.progressBar.percent += self.progressBar.increment
                self.progressBar.percent = (
                    100
                    if (self.progressBar.percent > 100)
                    else (self.progressBar.percent)
                )

                self.ptEmit()

            self.progressBar.text = LANG_DB[SELECTED_LANG][5]
            self.progressBar.percent = 100

        self.ptEmit()

        try:
            os.remove(NH_ENUMS.BREAKER_RES.value)
        except:
            pass

        await self.client.aclose()
