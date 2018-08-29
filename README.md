# iTunes to Rhythmbox playlist conversion
This script converts your iTunes playlists (saved in XML format) to a format usable by rhythmbox (also in XML).
This is done using the python's `xml.etree.ElementTree`, which provides a useful object-oriented interface for manipulating XML elements and files.
All you need to run this is a standard python installation (I tested this on 3.5). Open the file in your favorite text editor, and near the bottom you will see four strings and one list of strings:

`itunes_loc`: The location of your iTunes music library XML file.

`library_loc`: The location of the MP3 files on your local machine.

`rb_loc_from`: The location of your pre-existing Rhythmbox playlist file (this is usually found at `/home/user/.local/share/rhythmbox/playlist.xml`).

`rb_loc_to`: The location where you want to write your new Rhythmbox playlist file to. The file doesn't need to exist beforehand; a new one will be created with that name.

`playlists_to_remove`: A list of playlists that you don't want to import (it will attempt to import ALL playlists otherwise, even ones you didn't create, like the entire library or your top 25 songs etc.).

Just point the above variables to the appropriate location, specify the playlists you don't want to import, and go ahead and run the file in your python interpreter. If you have `rb_loc_to` set to something other than the default (default value of `rb_loc_from`) , you'll probably need to rename it to that so that Rhythmbox will recognize the playlist file.

If you'd like to know how it works, take a look at the header of the script, it has a fairly thorough explanation of the structure of the two files, and hopefully the comments throughout are sufficient to explain the methods.

This was last tested on 2018/09/29 with Python 3.6.5 and Rhythmbox 3.4.2.
