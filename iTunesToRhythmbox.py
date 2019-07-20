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
import re
import xml.etree.ElementTree as ET

class ITunesLibrary(object):
    def __init__(self, itunes_loc, library_loc):
        self.itunes_loc = itunes_loc        # Location of the iTunes XML file
        self.library_loc = library_loc      # Location of the MP3 files
        self.itunes_dict = {}               # Map from track ID to file location
        self.playlists = {}                 # Map from playlist name to list of track IDs
        self.old_itunes_loc = None          # Location of MP3 files as referenced by iTunes XML file

    def parseITunes(self):
        """ Parses the iTunes library file into a dictionary with iTunes trackID as keys and the file location as
        values. Also turns iTunes playlists into dictionaries as well. """
        # Parse xml into tree
        tree = ET.parse(self.itunes_loc)
        root = tree.getroot()

        # Get all track IDs and track metadata
        trackIDs = root.findall("./dict/[key='Tracks']/dict/key")
        metadata_ = root.findall("./dict/[key='Tracks']/dict/dict")
        # Iterate over all tracks
        for trackID, metadata in zip(trackIDs, metadata_):
            for i, e_i in enumerate(metadata):
                # Add file location to dictionary
                if e_i.text == "Location":
                    self.itunes_dict[trackID.text] = metadata[i+1].text

        # Get all playlists
        playlists = root.findall("./dict/array/dict")
        # Iterate over playlists
        for playlist in playlists:
            # Iterate over elements in playlist
            for i, e_i in enumerate(playlist):
                # Get name of playlist
                if e_i.text == "Name":
                    playlist_name = playlist[i+1].text
                # Get tracks in the playlist
                elif e_i.tag == "array":
                    trackIDs = [trackID.text for trackID in e_i.findall("./dict/integer")]
                    # Write playlist to dict
                    self.playlists[playlist_name] = trackIDs


    def findOldItunesLocation(self):
        """ Find the part of the file location string that prepends the old location of the music files stored in
        the iTunes xml. """
        assert len(self.itunes_dict) != 0, "No songs in the iTunes dictionary."
        # Get the very first file name in the dictionary
        sample_file_name = list(self.itunes_dict.values())[0]
        # Figure out how many leading characters to chop off
        char_to_ignore = sample_file_name.rfind(r"/")
        self.old_itunes_loc = sample_file_name[:char_to_ignore]

    def formatFileLocation(self):
        """ Chops off the leading .../ from .../MusicFile.mp3 and appends to the actual library location. """
        self.findOldItunesLocation()
        loc_str = self.library_loc.replace(" ", r"%20")     # Need to replace spaces with '%20' otherwise Rhythmbox
                                                            # can't recognize the file strings
        for trackID in self.itunes_dict:
            self.itunes_dict[trackID] = r"file://" + loc_str + self.itunes_dict[trackID][len(self.old_itunes_loc):]

    def generatePlaylistXML(self, rb_loc_from, rb_loc_to=None, playlists_to_remove=[]):
        """ Modifies the Rhythmbox playlist XML file to insert the new playlists. """
        if rb_loc_to is None:
            rb_loc_to = rb_loc_from

        # Parse the XML tree
        tree = ET.parse(rb_loc_from)
        root = tree.getroot()   # The <rhythmdb-playlists> node

        # Remove unwanted playlists (like entire library, etc)
        for name in playlists_to_remove:
            if name in self.playlists:
                del self.playlists[name]

        # Iterate over all the playlists to add
        for name in self.playlists:
            # Construct playlist element (don't really understand the attributes, but they work...)
            playlist = ET.Element("playlist", attrib={"name": name, "show-browser": "false", "browser-position": "180",
                                                      "search-type": "search-match", "type": "static"})
            playlist.text = "\n  "  # Formatting to keep the XML readable
            # Iterate over tracks in playlist
            for trackID in self.playlists[name]:
                # Append tracks to playlist
                track = ET.Element("location")
                track.text = self.itunes_dict[trackID]
                track.tail = "\n    "   # Formatting to keep the XML readable
                playlist.append(track)

            # Append playlist to root
            root.append(playlist)

        # Write to file
        tree.write(rb_loc_to, "UTF-8")


itunes_loc = "/media/ecotner/HDD/Users/27182_000/Music/iTunes/iTunes Music Library.xml"
library_loc = "/media/ecotner/HDD/Users/27182_000/Music/Saved"
rb_loc_from = "/home/ecotner/.local/share/rhythmbox/playlists_original.xml"
rb_loc_to = "/home/ecotner/.local/share/rhythmbox/playlists.xml"
playlists_to_remove = ["Library", "Downloaded", "Music", "90’s Music", "My Top Rated", "Recently Added",
                       "Recently Played", "Top 25 Most Played"]

if __name__ == "__main__":
    itunes_lib = ITunesLibrary(itunes_loc, library_loc)
    itunes_lib.parseITunes()
    itunes_lib.formatFileLocation()
    #print([name for name in itunes_lib.playlists])
    itunes_lib.generatePlaylistXML(rb_loc_from, rb_loc_to, playlists_to_remove)
