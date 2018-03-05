from nose.tools import *

from itunes import playlist_sorter as sorter

library = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Major Version</key><integer>1</integer>
    <key>Minor Version</key><integer>1</integer>
    <key>Tracks</key>
    <dict></dict>
    <key>Playlists</key>
    <array>
        <dict>
            <key>Name</key><string>Purchased</string>
            <key>Playlist Items</key>
            <array>
                <dict>
                    <key>Track ID</key><integer>10035</integer>
                </dict>
                <dict>
                    <key>Track ID</key><integer>10687</integer>
                </dict>
                <dict>
                    <key>Track ID</key><integer>10519</integer>
                </dict>
                <dict>
                    <key>Track ID</key><integer>10038</integer>
                </dict>
            </array>
        </dict>
        <dict>
            <key>Name</key><string>Voice Memos</string>
        </dict>
    </array>
</dict>
</plist>"""


def get_playlist_test():
    data = sorter.parse_data(library)
    assert_equal({
        'Name': 'Purchased',
        'Playlist Items': [
            { 'Track ID': 10035 },
            { 'Track ID': 10687 },
            { 'Track ID': 10519 },
            { 'Track ID': 10038 },
        ]
    }, sorter.get_playlist(data, 'Purchased'))
    assert_false(sorter.get_playlist(data, 'abc'))
    assert_false(sorter.get_playlist_names(None))
    assert_false(sorter.get_playlist_names([]))

def get_playlist_names_test():
    assert_list_equal(
            ['Purchased', 'Voice Memos'],
            sorter.get_playlist_names(sorter.parse_data(library)))
    assert_false(sorter.get_playlist_names(None))
    assert_false(sorter.get_playlist_names([]))

def parse_data_test():
    assert_dict_equal({
            'Major Version': 1,
            'Minor Version': 1,
            'Tracks': {},
            'Playlists': [{
                'Name': 'Purchased',
                'Playlist Items': [
                    { 'Track ID': 10035 },
                    { 'Track ID': 10687 },
                    { 'Track ID': 10519 },
                    { 'Track ID': 10038 },
                ]
            }, {
                'Name': 'Voice Memos',
            }],
    }, sorter.parse_data(library))

def sort_playlist_items_test():
    data = sorter.parse_data(library)
    playlist = sorter.get_playlist(data, 'Purchased')
    assert_list_equal([
            { 'Track ID': 10035 },
            { 'Track ID': 10687 },
            { 'Track ID': 10519 },
            { 'Track ID': 10038 },
    ], playlist['Playlist Items'])

    sorter.sort_playlist_items(playlist, sorter.SortingOrder.Ascending)
    assert_list_equal([
            { 'Track ID': 10035 },
            { 'Track ID': 10038 },
            { 'Track ID': 10519 },
            { 'Track ID': 10687 },
    ], playlist['Playlist Items'])

    sorter.sort_playlist_items(playlist, sorter.SortingOrder.Descending)
    assert_list_equal([
            { 'Track ID': 10687 },
            { 'Track ID': 10519 },
            { 'Track ID': 10038 },
            { 'Track ID': 10035 },
    ], playlist['Playlist Items'])
