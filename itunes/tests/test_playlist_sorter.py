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
        </dict>
        <dict>
            <key>Name</key><string>Voice Memos</string>
        </dict>
    </array>
</dict>
</plist>"""


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
            }, {
                'Name': 'Voice Memos',
            }],
    }, sorter.parse_data(library))
