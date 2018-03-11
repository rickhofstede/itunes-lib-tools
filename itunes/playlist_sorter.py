#!/opt/local/bin/python2.7

from operator import attrgetter

import argparse
import plistlib
import sys

file = "/Users/hofstederj/Documents/Temp/iTunes Music Library.xml"


class SortingOrder:
    Ascending, Descending = range(2)


def main():
    arg_parser = argparse.ArgumentParser(
            description='Sort iTunes playlist by track IDs.')
    arg_parser.add_argument('playlist', help='name of the playlist to be sorted')
    arg_parser.add_argument('-s', '--order',
            help='sorting order; ascending vs. descending', choices=['asc', 'desc'])
    args = arg_parser.parse_args()

    with open(file) as library:
        root = parse_data(library.read())
        playlists = get_playlist_names(root)
        if args.playlist not in playlists:
            print("Playlist '%s' could not be found. Exiting..." % args.playlist)
            sys.exit(1)

        order = SortingOrder.Ascending
        if args.order is not None:
            order = SortingOrder.Ascending if args.order == 'asc' else SortingOrder.Descending

        sort_playlist_items(get_playlist(root, args.playlist), order)
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
