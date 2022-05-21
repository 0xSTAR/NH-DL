from enum import (
    Enum,
    unique,
    auto
)

@unique
class NH_ENUMS(Enum):
    BASE_LNK = "https://nhentai.net/g/"
    SUPER_BASED_LNK = "https://nhentai.net"

    NH_API = "https://nhentai.net/api/gallery/"
    IMG_URL = "https://i.nhentai.net/galleries/"

    CONFIG = "nh.ini"
