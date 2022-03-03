version:list = [1,0,0]
release_type:str = "dev"

print(
    "\nnh-dl v{}.{}.{}-{}\n-------------------\n".format(
        str(version[0]),
        str(version[1]),
        str(version[2]),
        release_type
    )
)

artist = {
    "At":"@",
    "Platform":""
}

artist_mention:str = "Artwork by {} on {}".format(artist["At"],artist["Platform"])