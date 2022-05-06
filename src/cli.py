#!/usr/bin/env python3

# COMMAND LINE INTERFACE

import sys
import os
from nhentai import (
    Thread,
    Client,
    Progress,
    sift,
    download
)
import startup
import asyncio
from math import floor as flr

class NHentai_Vanilla(object):
    def __init__(self, code:str, savedir:str):

        super().__init__()
        self.__code:str = str(code)
        self.__folder = "{}/{}/".format(
            str(savedir), self.__code
        )
        self.progressBar = Progress()
        self.client = Client.create_client()

    def run(self) -> str:
        try:
            os.mkdir(path=str(self.__folder), mode=511, dir_fd=None)
        except FileExistsError:
            pass

        asyncio.run(self.run_async())

    async def run_async(self):
        print(f"\nFetching No. {self.__code}\n")
        i = 1
        async for lnk in sift(self.client, self.progressBar, self.__code):

            x = await download(self.client, lnk.lnk, lnk.filename, self.__folder)

            self.progressBar.percent += self.progressBar.increment
            self.progressBar.percent = 100 if (self.progressBar.percent > 100) else (
                    self.progressBar.percent
                )

            print(f"Downloading page #{i} [{flr(self.progressBar.percent)}%]")
            i+=1

        await self.client.aclose()


class NH_CLI(object):
    def __init__(self, code:str):
        self.__code:str = str(code)
        #self.session = Client.create_client()
        self.saveToDirectory = os.getcwd().replace("\\","/").replace("//","/")


    def run(self):
        if (
            len(self.__code) == 0x6 and
            type(int(self.__code[0])) == int and
            type(int(self.__code[1])) == int and
            type(int(self.__code[2])) == int and
            type(int(self.__code[3])) == int and
            type(int(self.__code[4])) == int and
            type(int(self.__code[5])) == int
        ):
            print("Creating extractor instance...")
            self.nh_instance = NHentai_Vanilla(self.__code, self.saveToDirectory)#, self.session)
            print("Instantiating extractor worker thread...")
            self.nh_thread = Thread(target=self.nh_instance.run)

            print("\nBeginning Download...")
            self.nh_thread.start()

            self.nh_thread.join()
            print("Download ended.\n")

            print("Destroying extractor worker thread...")
            del(self.nh_thread)
            print("Extractor worker thread destroyed.")
            print("Destroying extractor instance...")
            del(self.nh_instance)
            print("Extractor instance destroyed.")


            print("\nFinished!\nThank you for using my service!\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"Code: {sys.argv[1]}")
        nh = NH_CLI(sys.argv[1])
        nh.run()

    else:
        print("ERROR: Must provide a sauce code.")
        print("Ex: NH 177013")
