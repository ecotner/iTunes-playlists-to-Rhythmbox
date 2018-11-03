import xml.etree.ElementTree as ET

PLAYLIST_FILE = '~/.local/share/rhythmbox/playlist_copy.xml'

tree = ET.parse(PLAYLIST_FILE)
root = tree.getroot()

for playlist in root:
    if playlist.attrib['type'] == 'static':
        playlist = sort_playlist(playlist)

