import os
import configparser
from nh_enums import NH_ENUMS

# change when building to switch the app to another language
SELECTED_LANG: str = "en"  # DEFAULT to ENGLISH

"""
SUPPORTED CURRENTLY:

"en" - English
"tr" - Turkish
"jp" - Japanese
"""

LANGS: list = [
    "en",  # english
    "tr",  # turkish
    "jp",  # japanese
]

_conf_fn: str = NH_ENUMS.CONFIG.value
if os.path.isfile(_conf_fn):
    LC = configparser.ConfigParser()
    try:
        LC.read(_conf_fn)
        _ldecl: str = LC["NH"]["LANGUAGE"].lower()
    except:
        _ldecl: str = "en"
    finally:
        SELECTED_LANG = _ldecl if (_ldecl in LANGS) else "en"

    del LC
    del _ldecl

del _conf_fn

LANG_DB: dict = {
    "en": [
        "6-Digit Code",
        "Save Directory",
        "Change Directory",
        "Fetching...",
        "Downloading...",
        "Finished!",
        "Idling...",
        "DL",
        "ERROR",
    ],
    "tr": [
        "6-Digit kod",
        "kayıt dosyası",
        "dosyayı değiştir",
        "Data alınıyor",
        "Indiriyor",
        "Biti",
        "rölanti",
        "DL",
        "Hatta",
        "Kurmayı başlatın",
    ],
    "jp": [
        "コード/六桁コード",
        "SAVE FOLDER",
        "CHANGE FOLDER",
        "フェッチ",
        "ダウンロード",
        "終了",
        "アイドル",
        "DL",
        "エラー",
    ],
}
