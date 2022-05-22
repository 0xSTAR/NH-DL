import io
import json
from httpx import Cookies
from nh_enums import NH_ENUMS
import os
import subprocess
import platform

__SYSTEM = platform.system()

__INTERP: str = NH_ENUMS.INTERP.value if not (__SYSTEM == "Windows") else r'.\node_interp\node'
if (__SYSTEM == "Linux"):
    __INTERP = "./node_interp/bin/node"
__BREAKER_RES: str = NH_ENUMS.BREAKER_RES.value
__BREAKER_DOR: str = NH_ENUMS.BREAKER_DOR.value

async def GET_BREAK_IT(X_L: str) -> Cookies:
    LNK_TO_BREAK:str = str(X_L)
    #__COOKIES = Cookies()
    FORMAT_CMD = "{} {} {}".format(__INTERP, __BREAKER_DOR, LNK_TO_BREAK)
    #print(FORMAT_CMD)
    os.system(FORMAT_CMD)
    #subprocess.check_call(
    #    [
    #        __INTERP,
    #        __BREAK_DOR,
    #        LNK_TO_BREAK
    #    ]
    #)
    __F = io.open(__BREAKER_RES,mode="r")
    try:
        x = json.loads(__F.read())

        #for _C in x:
        #    __COOKIES.set(_C["name"],_C["value"],domain=_C["domain"],path=_C["path"])
    except:
        raise Exception()
    finally:
        __F.close()
    return x

#GET_BREAK_IT()
