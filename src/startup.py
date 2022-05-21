version:list = [1,1,1]
release_type:str = "dev"

print(
    "\nnh-dl v{}.{}.{}-{}\n-------------------\n".format(
        str(version[0]),
        str(version[1]),
        str(version[2]),
        release_type
    )
)
