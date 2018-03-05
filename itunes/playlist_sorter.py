#!/opt/local/bin/python2.7

import plistlib

file = "/Users/hofstederj/Documents/Temp/iTunes Music Library.xml"


def main():
    with open(file) as library:
        root = parse_data(library.read())

def parse_data(data):
    '''Read iTunes library's XML/PList file and return root element'''
    return plistlib.readPlistFromString(data)

if __name__ == "__main__":
    main()
