# SC_3380_Project

# MYSQL Initialization
  1. In mySQL workbench, connect to local
  2. File > Open SQL Script, and open makedb.sql
  3. After making database, open datainput.sql

# Python Initialization
(This application is made in Python 3.9.13, virtual environment)

pip install -r requirements.txt

# HOW it works
Implemented features 1 through 6 that I wrote in Phase 2. 
I assumed the user is logged in with a userId "user1".
There are 3 buttons,
Make Playlist
Subscribe Playlist
Go To My Playlists

[Make Playlist]
User can search the song to make his or her own playlist.
The songs which titles are song# and music# are in the database. 
User can Add them to Playlist using 'Add to Playlist' button.

After adding all the songs, user can press 'Confirm' button to enter other information about the playlist.

[Subscribe Playlist]
User can search for the name of a playlist.
The search results exclude playlists to which the user is already subscribed. 

[Go To My Playlists]
User can view 'my playlist'
User can modify the songs, the privilege on the playlist if it is private playlist.
User can listen to the music pressing the 'Listen' button.



