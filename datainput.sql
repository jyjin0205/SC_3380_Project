USE playlist;

INSERT INTO USER (Id, Name, Password, Age) VALUES
("user1", "user1", "password", 20),
("user2", "user2", "password", 20),
("user3", "user3", "password", 20),
("user4", "user4", "password", 20),
("my1", "my1", "password", 20),
("my2", "my2", "password", 20),
("my3", "my3", "password", 20),
("my4", "my4", "password", 20),
("my5", "my5", "password", 20),
("my6", "my6", "password", 20);

INSERT INTO admin (Id, Name, Division) VALUES
("admin1", "admin1",  "admin1div");

INSERT INTO MUSIC (Id, File, Title) VALUES
("song1","filelink","song1"),
("song2","filelink","song2"),
("song3","filelink","song3"),
("song4","filelink","song4"),
("song5","filelink","song5"),
("song6","filelink","song6"),
("song7","filelink","song7"),
("song8","filelink","song8"),
("song9","filelink","song9"),
("song10","filelink","music1"),
("song11","filelink","music2"),
("song12","filelink","music3"),
("song13","filelink","music4"),
("song14","filelink","music5"),
("song15","filelink","music6"),
("song16","filelink","music7"),
("song17","filelink","music8"),
("song18","filelink","music9"),
("song19","filelink","music10");

INSERT INTO ARTIST (Id, Name) VALUES
("art1","songartist"),
("art2","musicartist");

INSERT INTO ARTISTMUSIC (Music_id, Artist_id) VALUES
("song1","art1"),
("song3","art1"),
("song5","art1"),
("song10","art2"),
("song12","art2"),
("song14","art2"),
("song9","art1"),
("song9","art2");

INSERT INTO PLAYLIST (Id,Name,Description,Sharing_type) VALUES
("playlist1","Num1","The playlist of number 1",1),

("playlist2","Num2","The playlist of number 2",1);

INSERT INTO PLAYLIST (Id,Name,Description,Sharing_type,Creater_id,Creater_description) VALUES
("Official1","Official1","It is official playlist 1",1,"admin1","admin1 created it"),
("Official2","Official2","It is official playlist 2",1,"admin1","admin1 created it again");

INSERT INTO PLAYLISTMUSIC (Playlist_id,Music_id) VALUES
("playlist1","song1"),
("playlist1","song10"),

("playlist2","song2"),

("playlist2","song12");

INSERT INTO PLAYLISTMUSIC (Playlist_id,Music_id) VALUES
("Official1","song1"),
("Official2","song10");