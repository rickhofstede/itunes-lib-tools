#!/opt/local/bin/python2.7

import plistlib

file = "/Users/hofstederj/Documents/Temp/iTunes Music Library.xml"


def main():
    with open(file) as library:
        root = parse_data(library.read())
        playlists = get_playlist_names(root)

def get_playlist_names(data):
    '''Extract playlist names from read data'''
    if not data or not 'Playlists' in data:
        return False

    return [ playlist['Name'] for playlist in data['Playlists'] ]

def parse_data(data):
    '''Read iTunes library's XML/PList file and return root element'''
    return plistlib.readPlistFromString(data)

if __name__ == "__main__":
    main()
