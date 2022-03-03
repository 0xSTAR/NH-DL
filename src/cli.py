#!/usr/bin/env python3

# COMMAND LINE INTERFACE

import sys
import os
from nhentai import (
    Thread, 
    Session,
    Progress, 
    sift, 
    download
)
import startup

class NHentai_Vanilla(object):
    def __init__(self, code:str, savedir:str, session:Session):
        super().__init__()
        self.__code:str = str(code)
        self.__folder = "{}/{}/".format(
            str(savedir), self.__code
        )

        self.session = session
        self.progressBar = Progress()

    def run(self) -> str:
        try:
            os.mkdir(path=str(self.__folder), mode=511, dir_fd=None)
        except FileExistsError:
            pass

        os.chdir(self.__folder)

        for lnk in sift(self.session, self.progressBar, self.__code):
            download(self.session, lnk.lnk, lnk.filename)


class NH_CLI(object):
    def __init__(self, code:str):
        self.__code:str = str(code)
        self.session = Session()
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
            self.nh_instance = NHentai_Vanilla(self.__code, self.saveToDirectory, self.session)
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


            print("\nFinished.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"Code: {sys.argv[1]}")
        nh = NH_CLI(sys.argv[1])
        nh.run()

    else:
        print("ERROR: Must provide a sauce code.")
        print("Ex: NH 177013")