import re
from os import path, walk

class HexData:
    before = None
    after = None
    def __init__(self, bef=None, aft=None):
        self.before = bytes.fromhex(bef)
        self.after = bytes.fromhex(aft)

dict_data = {
    "2018.1" : HexData("84 C0 75 08 33 C0 48 83 C4 30", "84 C0 74 08 33 C0 48 83 C4 30"),
    "2018.2" : HexData("84 C0 75 08 33 C0 48 83 C4 30", "84 C0 74 08 33 C0 48 83 C4 30"),
    "2018.3" : HexData("84 C0 75 08 33 C0 48 83 C4 30", "84 C0 74 08 33 C0 48 83 C4 30"),
    "2018.4" : HexData("74 04 33 C0 EB 02 8B 03 48 8B 4C", "75 04 33 C0 EB 02 8B 03 48 8B 4C"),
    "2019.1" : HexData("74 04 33 C0 EB 02 8B 07", "75 04 33 C0 EB 02 8B 07"),
    "2019.2" : HexData("75 15 33 C0 EB 13 90", "74 15 33 C0 EB 13 90"),
    "2019.3" : HexData("75 15 33 C0 EB 13 90", "74 15 33 C0 EB 13 90")
}

def find_exe(version):
    ex = re.compile(version.replace(".", r"\.") + r"\.[0-9]{1,2}[abf][0-9]")

    filepath = ""
    progfile = "C:\\Program Files\\Unity\\"
    progfile86 = "C:\\Program Files (x86)\\Unity\\"

    if path.exists(progfile86):
        filepath = progfile86

    if path.exists(progfile):
        filepath = progfile

    for (_, dirnames, _) in walk(filepath):
        for dirname in dirnames:
            match = ex.match(dirname)
            if match != None:
                return filepath + match.string + "\\Editor\\Unity.exe"
        break
    
    print("Could not find Unity.exe")
    exit(0)

print("Currently Windows Only")

print("Unity Versions: ")
for key in dict_data:
    print(key)
print("Select Version: ")
version = input()
hexdata = None
if version in dict_data:
    hexdata = dict_data[version]
else:
    print("No hex values for that version")
    exit(0)

filename = find_exe(version)

data = None
with open(filename,"rb") as f:
    data=bytearray(f.read())
data=data.replace(hexdata.before, hexdata.after)
with open("Unity.exe","wb") as f:
    f.write(data)
print("Copy \"" + path.abspath("Unity.exe") + "\" to \"" + filename +"\"")