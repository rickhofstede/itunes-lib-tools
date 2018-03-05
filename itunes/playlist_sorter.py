#!/opt/local/bin/python2.7

from operator import attrgetter

import plistlib
import sys

file = "/Users/hofstederj/Documents/Temp/iTunes Music Library.xml"
playlist = 'Purchased'


class SortingOrder:
    Ascending, Descending = range(2)


def main():
    with open(file) as library:
        root = parse_data(library.read())
        playlists = get_playlist_names(root)
        if playlist not in playlists:
            print("Playlist '%s' could not be found. Exiting..." % playlist)
            sys.exit(1)

        sort_playlist_items(get_playlist(root, playlist), SortingOrder.Ascending)
        plistlib.writePlist(root, file + ".new")

def get_playlist(data, name):
    '''Extract playlist from read data'''
    if not name in get_playlist_names(data):
        return False

    for playlist in data['Playlists']:
        if playlist['Name'] == name:
            return playlist
    return False

def get_playlist_names(data):
    '''Extract playlist names from read data'''
    if not data or not 'Playlists' in data:
        return False

    return [ playlist['Name'] for playlist in data['Playlists'] ]

def parse_data(data):
    '''Read iTunes library's XML/PList file and return root element'''
    return plistlib.readPlistFromString(data)

def sort_playlist_items(playlist, order):
    '''Sort playlist items'''
    if not 'Playlist Items' in playlist:
        return False

    items = playlist['Playlist Items']
    items.sort(key=attrgetter('Track ID'), reverse=(order == SortingOrder.Descending))
    return items

if __name__ == "__main__":
    main()
