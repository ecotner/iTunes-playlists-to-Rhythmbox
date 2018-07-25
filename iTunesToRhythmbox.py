"""
Date: July 25, 2018
Author: Eric Cotner

Converts iTunes playlists to Rhythmbox playlists. Simply point <itunes_loc> to the your 'iTunes Music Library.xml' file,
<rb_loc> to the location of your Rhythmbox playlist (usually ~/.local/share/rhythmbox/playlists.xml), and <library_loc>
to the directory where all your music is stored.

The iTunes file stores all songs in an xml structure of the form
<dict>
    ... (other structures)
    <key>Tracks</key>
    <dict>
        <key><track ID></key>
        <dict>
            <key>Track ID</key><integer><track ID></integer>
            ... (more attributes)
            <key>Location</key><string><file location></string>
            ... (more attributes)
        </dict>
        ... (more tracks)
    </dict>
    ... (other structures)
</dict>

We basically want to first extract the track ID and file location. iTunes then uses the track ID to make all internal
references to the song, including in playlists. The playlists are stored in the form
<dict>
    ...
    <key>Playlists</key>
    <dict>
        <dict>
            ... (other attributes)
            <key>Name</key><string>playlist_name</string>
            <key>Playlist Items</key>
            <array>
                <dict>
                    <key>Track ID</key><integer>track_id</integer>
                </dict>
                ... (other tracks)
            </array>
        </dict>
        ... (other playlists)
    </dict>
</dict>

The Rhythmbox playlist is much simpler.
<rhythmdb-playlists>
    <playlist name=playlist_name show-browser="false" browser-position="180" type="static"
        <location>file_location</location>
        ... (other files)
    </playlist>
</rhythmdb-playlists>

"""

import pandas as pd

itunes_loc = "/media/ecotner/Data HDD/Users/27182_000/Music/iTunes/iTunes Music Library.xml"
rb_loc = "~/.local/share/rhythmbox/playlists.xml"
library_loc = "/media/ecotner/Data HDD/Users/27182_000/Music/Saved"

class ITunesLibrary(object):
    def __init__(self, itunes_loc, library_loc):
        self.itunes_loc = itunes_loc
        self.library_loc = library_loc
        self.itunes_dict = None

    def parseITunes(self):
        """ Parses the iTunes library file into a dictionary"""
        with open(self.itunes_loc, "r") as fo:
            for line in fo.readlines():



itunes_lib = ITunesLibrary(itunes_loc, library_loc)
itunes_lib.parseITunes()
print(itunes_lib.itunes_dict)