#!/opt/local/bin/python2.7

from operator import attrgetter

import argparse
import os.path
import plistlib
import sys


class SortingOrder:
    Ascending, Descending = range(2)


def main():
    arg_parser = argparse.ArgumentParser(
            description='Sort iTunes playlist by track IDs.')
    arg_parser.add_argument('library', help='path to iTunes library')
    arg_parser.add_argument('playlist', help='name of the playlist to be sorted')
    arg_parser.add_argument('-o', '--output', help='output file name')
    arg_parser.add_argument('-s', '--order',
            help='sorting order; ascending vs. descending', choices=['asc', 'desc'])
    args = arg_parser.parse_args()

    if not os.path.isfile(args.library):
        print("iTunes library '%s' could not be found. Exiting..." % args.library)
        sys.exit(1)

    if args.output is None or True:
        file = os.path.basename(args.library)
        path = os.path.dirname(args.library)
        out_file = "%s/%s_new.xml" % (path, os.path.splitext(file)[0])
    else:
        out_file = args.output

    with open(args.library) as library:
        root = parse_data(library.read())
        playlists = get_playlist_names(root)
        if args.playlist not in playlists:
            print("Playlist '%s' could not be found. Exiting..." % args.playlist)
            sys.exit(1)

        order = SortingOrder.Ascending
        if args.order is not None:
            order = SortingOrder.Ascending if args.order == 'asc' else SortingOrder.Descending

        sort_playlist_items(get_playlist(root, args.playlist), order)
        plistlib.writePlist(root, out_file)

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
