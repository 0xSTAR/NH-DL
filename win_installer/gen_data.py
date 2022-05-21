DATA_OUT_FILE = "data.py"

dist = "./../dist/"

root_files = {0: "NH.exe", 1: "conf.ini"}

content = "./../dist/content/"
content_files = {0: "bg0.png", 1: "nh0.png"}

root_data = []
content_data = []

# filling the binary data in
for i in range(len(root_files)):
    try:

        with open(dist + root_files[i], "rb") as _file:
            root_data.append(_file.read())
    except:
        with open(dist + root_files[i], "r") as _file:
            root_data.append(_file.read())

for i in range(len(content_files)):
    try:

        with open(content + content_files[i], "rb") as _file:
            content_data.append(_file.read())
    except:
        with open(content + content_files[i], "r") as _file:
            content_data.append(_file.read())

data = "root_data = []\ncontent_data=[]\n"

for d in root_data:
    data += "root_data.append({})\n".format(str(d))

for d in content_data:
    data += "content_data.append({})\n".format(str(d))

with open(DATA_OUT_FILE, "w") as __dest:
    __dest.write(data)
