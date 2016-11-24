import unicodedata
import sys

def normalize_utf8(norm='NFC', data='./'):
    with open(data, "r") as f:
        l = f.readlines()
        l = [unicodedata.normalize(norm, s).strip(' ') for s in l]
    with open(data, 'w') as f:
        [f.write(s) for s in l]

normalize_utf8(norm=sys.argv[1], data=sys.argv[2])