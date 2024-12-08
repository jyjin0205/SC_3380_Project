import mysql.connector
import PySimpleGUI as sg
import uuid

####### global variable #########
making_playlist_id = None
userId = "user1"
selectedSongs = []
sendingSongs = []
sendingPlaylists = []
sendingUserName = []
number = 1

####### Database Connect ###########
mydb = mysql.connector.connect(
    host="127.0.0.1", #localhost
    user='root',
    password='dbwls6bnqhv',
    database='playlist'
)

mycursor = mydb.cursor()

'''
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)
'''

####### Query Function ###########
#Func1 : User_make_the_playlist
#Search Music from Title
def function1(songTitle):
    query = "SELECT * FROM MUSIC WHERE Title LIKE %s"
    songTitle = f"%{songTitle}%" # f-string use
    mycursor.execute(query,(songTitle,))
    myresult = mycursor.fetchall()

    return myresult

#Search Artist's Id from musicId
#And search Artist's info from Artist's Id
def function1_1(musicId):
    query = "SELECT Artist_id FROM ARTISTMUSIC WHERE Music_id = %s"
    mycursor.execute(query,(musicId,))
    myresult = mycursor.fetchall()

    if not myresult:
        return None
    
    result = []
    
    query = "SELECT * FROM ARTIST WHERE Id = %s"
    for artist in myresult:
        mycursor.execute(query,(artist[0],))
        result.append(mycursor.fetchone())
    
    if not result:
        return None
    return result

#Make new playlist
def function1_2(playlistId,name,desc,sharing_type):
    query = "INSERT INTO PLAYLIST (Id, Name, Description, Sharing_type) VALUES (%s,%s,%s,%s)"
    mycursor.execute(query,(playlistId,name,desc,sharing_type,))
    mydb.commit()

#Make user-playlist relationship
def function1_3(userId,playlistId,owning_status):
    query = "INSERT INTO USERPLAYLIST (User_id, Playlist_id) VALUES(%s, %s)"
    mycursor.execute(query,(userId,playlistId,))
    mydb.commit()

    query = "INSERT INTO USERPLAYLIST_OWNINGSTATUS (User_id, Playlist_id,Owning_status) VALUES(%s, %s, %s)"
    mycursor.execute(query,(userId,playlistId,owning_status,))
    mydb.commit()
    

#Add Songs to Playlists using musicId and playlistId
def function1_4(musicId, playlistId):
    if not musicId:
        return "Music Id Error"
    if not playlistId:
        return "Playlist Id Error"
    
    query = """SELECT EXISTS(
        SELECT 1
        FROM PLAYLISTMUSIC as PM
        WHERE PM.Playlist_id = %s
        AND PM.Music_id = %s
    );"""
    mycursor.execute(query,(playlistId,musicId,))
    myresult = mycursor.fetchall()

    if myresult[0][0]:
        return "This Music Already Exist"
    
    query = "INSERT INTO PLAYLISTMUSIC (Playlist_id,Music_id) VALUES(%s, %s)"
    mycursor.execute(query,(playlistId,musicId,))
    mydb.commit()

    return None


#Func2 : User_Subscribe_the_playlist
def function2(userId, playlistName):
    query = """
        SELECT * FROM PLAYLIST p 
        WHERE p.Sharing_type = 1 
        AND p.Name LIKE %s
        AND NOT EXISTS(
            SELECT 1
            FROM USERPLAYLIST u
            WHERE u.User_id = %s
            AND u.Playlist_id = p.Id
        )
    """
    playlist = f"%{playlistName}%" # f-string use
    mycursor.execute(query,(playlist,userId))
    myresult = mycursor.fetchall()

    return myresult

#Func3 : User_Modify_the_permission
#Search a userName who is not subscribe playlistId
def function3(userName,playlistId):
    query = """
        SELECT * FROM USER u 
        WHERE p.Name LIKE %s
        AND NOT EXISTS(
            SELECT 1
            FROM USERPLAYLIST up
            WHERE up.Playlist_id = %s
            AND up.User_id = u.Id
        )
    """
    playName = f"%{userName}%" # f-string use
    mycursor.execute(query,(playName,playlistId))
    myresult = mycursor.fetchall()

    return myresult

#Func4 : User_MODIFY_the_playlist
#Search all music id's in the playlist
def function4(playlistId):
    query = "SELECT * FROM PLAYLISTMUSIC WHERE Playlist_id = %s"
    mycursor.execute(query,(playlistId,))
    myresult = mycursor.fetchall()

    if not myresult:
        return "No Playlist's Music"
    
    result = []
    for music in myresult:
        query = "SELECT * FROM MUSIC WHERE Id = %s"
        mycursor.execute(query,(music[1],))
        result.append(mycursor.fetchone())

    return result


#Func5 : User_See_the_playlist
#Default UserId is user1
#Search User's Playlist
def function5(userId):
    query = "SELECT Playlist_id FROM USERPLAYLIST WHERE User_id = %s"
    mycursor.execute(query,(userId,))
    myresult = mycursor.fetchall()
    #for x in myresult:
    #    print(x)

    return myresult

#Search Playlist's Info by playlistId
def function5_1(playlistId):
    query = "SELECT * FROM PLAYLIST WHERE Id = %s"
    mycursor.execute(query,(playlistId,))
    myresult = mycursor.fetchone()

    return myresult #one tuple

#Search Playlist's OwningStatus by playlistId
def function5_2(userId, playlistId):
    query = "SELECT Owning_status FROM USERPLAYLIST_OWNINGSTATUS WHERE User_id = %s AND Playlist_id = %s"
    mycursor.execute(query,(userId,playlistId,))
    myresult = mycursor.fetchone()

    return myresult #one tuple

#Delete Playlist's song if the song isn't the only song of it
def function5_3(playlistId, musicId):
    query = "SELECT COUNT(*) FROM PLAYLISTMUSIC WHERE Playlist_id = %s"
    mycursor.execute(query,(playlistId,))
    myresult = mycursor.fetchone()

    if myresult[0] <= 1:
        return "The playlist must have at least one song"

    query = "DELETE FROM PLAYLISTMUSIC WHERE Playlist_id = %s AND Music_id = %s"
    mycursor.execute(query,(playlistId,musicId,))
    mydb.commit()
    return None

#Set User's Playback operation
#It can be 1, 2, 3, 4. 1 means ‘one song repeat’, 2 means ‘whole part repeat’, 
#3 means ‘repeat randomly’, 4 means ‘play once’ 
def function6(a):
    if a not in ["1","2","3","4"]:
        return None
    query = "UPDATE USER SET Playback_operation = %s WHERE Id = %s"
    mycursor.execute(query,(a,userId))
    mydb.commit()

    return None

#Set User's Playback_status
#It can be 0 or 1. 0 means ‘paused’, 1 means ‘playing’
def function6_1():
    return None

#Set User's Playing_song
def function6_2(musicId):
    query = "UPDATE USER SET Current_playlist = %s WHERE Id = %s"
    mycursor.execute(query,(musicId,userId,))
    mydb.commit()
    return None

#Get User's Next song
def function6_3():
    return None

##########layout part##########

###### GUI Function #######

def go_main():
    window.write_event_value("Main",None)


def create_main_btn(layout):
    layout.append([sg.Button("Main")])
    return layout

def create_main_layout():
    make_playlist = [
    [sg.Button("Make Playlist")]
    ]

    subscribe_playlist = [
        [sg.Button("SubScribe Playlist")]
    ]

    my_playlists = [
        [sg.Button("Go To My Playlists")]
    ]
    main_layout = [make_playlist,subscribe_playlist,my_playlists]
    return main_layout

def create_main_playlist_layout():
    make_playlist_layout = [
    [sg.Text("Insert Songs"),sg.Button("Main")],
    [sg.In(key="-Songs_INPUT-"), sg.Button("Search Song")],
    [sg.Text("",key="MAKE_PLAYLIST_TITLE")],
    [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_1"),sg.Button("Add to Playlist",key="ADDPLAY_1",disabled=True, visible=False)],
    [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_2"),sg.Button("Add to Playlist",key="ADDPLAY_2",disabled=True, visible=False)],
    [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_3"),sg.Button("Add to Playlist",key="ADDPLAY_3",disabled=True, visible=False)],
    [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_4"),sg.Button("Add to Playlist",key="ADDPLAY_4",disabled=True, visible=False)],
    [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_5"),sg.Button("Add to Playlist",key="ADDPLAY_5",disabled=True, visible=False)],
    [sg.Button("Confilm", key="MAKE_PLAYLIST_BUTTON", disabled=True, visible=False)]
    ]

    return make_playlist_layout

def create_main_playlist_confilm_layout():
    make_playlist_confilm_layout = [
    [sg.Text("Insert Playlist's Name:")],
    [sg.In(key="-Name_INPUT-")],
    [sg.Text("Insert Description:")],
    [sg.In(key="-Description_INPUT-")],
    [sg.Text("Choose Sharing Type")],
    [sg.Radio("Public", "RADIO_GROUP", key="-Public-",default=True)],
    [sg.Radio("Private", "RADIO_GROUP", key="-Private-")],
    [sg.Button("Confilm", key="MAKE_PLAYLIST_BUTTON2")]
    ]

    return make_playlist_confilm_layout

def create_subscribe_playlist_layout():
    subscribe_playlist_layout = [
        [sg.Text("Subscribe"),sg.Button("Main")],
        [sg.In(key="-Subscribe_INPUT-"),sg.Button("Search Playlist")],
        [sg.Text("",key="SUBSCRIBE_PLAYLIST_TITLE")],
        [sg.Text("",key="SUBSCRIBE_INFO_1"),sg.Button("Add to My Playlist",key="ADDMYPLAY_1",disabled=True, visible=False)],
        [sg.Text("",key="SUBSCRIBE_INFO_2"),sg.Button("Add to My Playlist",key="ADDMYPLAY_2",disabled=True, visible=False)],
        [sg.Text("",key="SUBSCRIBE_INFO_3"),sg.Button("Add to My Playlist",key="ADDMYPLAY_3",disabled=True, visible=False)],
        [sg.Text("",key="SUBSCRIBE_INFO_4"),sg.Button("Add to My Playlist",key="ADDMYPLAY_4",disabled=True, visible=False)],
        [sg.Text("",key="SUBSCRIBE_INFO_5"),sg.Button("Add to My Playlist",key="ADDMYPLAY_5",disabled=True, visible=False)]
    ] 
    return subscribe_playlist_layout  

def create_my_playlists_layout():
    my_playlists_layout = [
        [sg.Text("Your Playlists"),sg.Button("Main")],
    ]    

    myresult = function5(userId)
    if not myresult :
        my_playlists_layout.append([sg.Text("You don't have Playlist",key="MY_PLAYLISTS_TITLE")])
        return my_playlists_layout

    my_playlists_layout.append([sg.Text("You have "+str(len(myresult))+" playlists",key="MY_PLAYLISTS_TITLE")])
    for playlistId in myresult:
        playlistId = playlistId[0]
        playlistInfo = function5_1(playlistId)
        OwningStatus = function5_2(userId,playlistId)
        layout_part = [sg.Text("Playlist's Name: "+ playlistInfo[1]),
                        sg.Text(playlistInfo[2]),
                        sg.Text("Public Playlist") if playlistInfo[3] else sg.Text("Private Playlist"),
                        sg.Text("Owner") if OwningStatus[0] == 1 else sg.Text("Subscriber")
                        ]
        my_playlists_layout.append(layout_part)
        layout_part2=[sg.Button("Listen",key=f"Listen_{playlistId}")]
        #If user is owner
        if OwningStatus[0] == 1:
            if playlistInfo[3] == 0:
                layout_part2.append(sg.Button("Modify Permission",key=f"ModifyPermission_{playlistId}"))
        
        #If user can modify it
        if OwningStatus[0] == 1 or OwningStatus[0] == 2 :
            layout_part2.append(sg.Button("Modify Songs",key=f"ModifySongs_{playlistId}"))
        
        
        my_playlists_layout.append(layout_part2)
    return my_playlists_layout

def create_modify_permission_layout(playlistId):
    default_modify_permission_layout = [
        [sg.Text("Your "),sg.Text("",key="-YOUR_PLAYLIST_NAME-"),sg.Button("Main")],
        [sg.In(key="-USERNAME_INPUT-")],
        [sg.Button("Search User",key=f"SearchUser_{playlistId}")],
        [sg.Text("",key="MODIFY_PERMISSION_TITLE")],
        [sg.Text("",key="MP_1"),sg.Button("Add User",key=f"ADDMP_{playlistId}_1",disabled=True, visible=False)],
        [sg.Text("",key="MP_2"),sg.Button("Add User",key=f"ADDMP_{playlistId}_2",disabled=True, visible=False)],
        [sg.Text("",key="MP_3"),sg.Button("Add User",key=f"ADDMP_{playlistId}_3",disabled=True, visible=False)],
        [sg.Text("",key="MP_4"),sg.Button("Add User",key=f"ADDMP_{playlistId}_4",disabled=True, visible=False)],
        [sg.Text("",key="MP_5"),sg.Button("Add User",key=f"ADDMP_{playlistId}_5",disabled=True, visible=False)]
    
    ]

    return default_modify_permission_layout

def create_modify_playlist_layout(playlistId):
    modify_playlist_layout = [
        [sg.Text("Your"),sg.Text("",key="-YOUR_PLAYLIST_NAME-"),sg.Button("Main")],
        [sg.Button("Add Songs",key=f"ADDSONGMODIFY_{playlistId}")],
    ]

    songsInfo = function4(playlistId)
    if not songsInfo:
        modify_playlist_layout.append([sg.Text("NO Result of the song",key="MODIFY_PLAYLIST_TITLE")])
    else:
        modify_playlist_layout.append([sg.Text("Songs in the Playlist",key="MODIFY_PLAYLIST_TITLE")])
        for song in songsInfo:
            SongInfoText="Title: "+song[2]+"\n"
            artists = function1_1(song[0])
            if not artists:
                SongInfoText += "No Artist Info"
            else:
                SongInfoText += "Artists: "
                artistText=""
                for artist in artists:
                    artistText+=artist[1]+" "
                SongInfoText+=artistText
            modify_playlist_layout.append([sg.Text(SongInfoText),sg.Button("DELETE",key=f"DELETEMPP_{playlistId}_{song[0]}")])
    
    return modify_playlist_layout

def create_add_song_to_playlist_layout(playlistId):
    playlistInfo = function5_1(playlistId)
    add_song_layout = [
        [sg.Text("In Playlist: "+playlistInfo[1])], #not null
        [sg.Text("Enter Song Name"),sg.Button("Main")],
        [sg.In(key="-Songs_INPUT-"), sg.Button("Search Songs",key=f"SearchSong2_{playlistId}")],
        [sg.Text("",key="MAKE_PLAYLIST_TITLE")],
        [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_1"),sg.Button("Add to Playlist",key=f"ADDSONG_1_{playlistId}",disabled=True, visible=False)],
        [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_2"),sg.Button("Add to Playlist",key=f"ADDSONG_2_{playlistId}",disabled=True, visible=False)],
        [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_3"),sg.Button("Add to Playlist",key=f"ADDSONG_3_{playlistId}",disabled=True, visible=False)],
        [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_4"),sg.Button("Add to Playlist",key=f"ADDSONG_4_{playlistId}",disabled=True, visible=False)],
        [sg.Text("",key="MAKE_PLAYLIST_SONGINFO_5"),sg.Button("Add to Playlist",key=f"ADDSONG_5_{playlistId}",disabled=True, visible=False)]    
    ]
    return add_song_layout

def create_listen_layout(playlistId):
    songsInfo = function4(playlistId)
    listen_layout = []

    if not songsInfo:
        listen_layout.append([sg.Text("NO song",key="LISTEN_TITLE"),sg.Button("Main")])
    else:
        listen_layout.append([sg.Text("Songs in the Playlist",key="LISTEN_TITLE"),sg.Button("Main")])
        for song in songsInfo:
            SongInfoText="Title: "+song[2]+"\n"
            artists = function1_1(song[0])
            if not artists:
                SongInfoText += "No Artist Info"
            else:
                SongInfoText += "Artists: "
                artistText=""
                for artist in artists:
                    artistText+=artist[1]+" "
                SongInfoText+=artistText
            listen_layout.append([sg.Text(SongInfoText),sg.Button("PLAY",key=f"PLAYLISTEN_{playlistId}_{song[0]}_{song[2]}")])
    return listen_layout
    

##########GUI Part#########

# Create the window
window = sg.Window("DEMO", create_main_layout())

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "GO_MAIN" or event == "Main":
        window.close()
        new_layout = create_main_layout()
        window = sg.Window("DEMO",new_layout)

    if event == "Make Playlist":
        new_layout = create_main_playlist_layout()
        making_playlist_id = str(uuid.uuid4())
        window.close()
        window = sg.Window("DEMO", new_layout)
    
    #Make_Playlist_layout
    if event == "Search Song":
        user_input = values["-Songs_INPUT-"]
    
        #Reset
        for i in range(1,6):
            window["MAKE_PLAYLIST_SONGINFO_"+str(i)].update("")
            window["ADDPLAY_"+str(i)].update(visible=False)
            window["ADDPLAY_"+str(i)].update(disabled=True)

        if not user_input.strip():
            sg.popup("Enter a song title!")
        else:
            songsresult = function1(user_input)
            if not songsresult:
                window["MAKE_PLAYLIST_TITLE"].update("NO Result of the song title")
            else: 
                window["MAKE_PLAYLIST_TITLE"].update("Songs found:")
                sendingSongs = []
                count = 1
                for song in songsresult:
                    if count > 5:
                        break
                    sendingSongs.append(song[0])
                    SongInfoText="Title: "+ song[2]+"\n"
                    artists = function1_1(song[0])
                    if not artists:
                        SongInfoText += "No Artist Info"
                    else:
                        SongInfoText += "Artists: "
                        artistText=""
                        for artist in artists:
                            artistText+=artist[1]+" "
                        SongInfoText+=artistText
                    window["MAKE_PLAYLIST_SONGINFO_"+str(count)].update(SongInfoText)
                    window["ADDPLAY_"+str(count)].update(visible=True)
                    window["ADDPLAY_"+str(count)].update(disabled=False)
                    count += 1
                
        window["-Songs_INPUT-"].update(value="")

    if event.startswith("SearchSong_"): 
        playlistId = event.split("_")[1]
        user_input = values["-Songs_INPUT-"]

        #Reset
        for i in range(1,6):
            window["MAKE_PLAYLIST_SONGINFO_"+str(i)].update("")
            window["ADDPLAY_"+str(i)].update(visible=False)
            window["ADDPLAY_"+str(i)].update(disabled=True)

        if not user_input.strip():
            sg.popup("Enter a song title!")
        else:
            songsresult = function1(user_input)
            if not songsresult:
                window["MAKE_PLAYLIST_TITLE"].update("NO Result of the song title")
            else: 
                window["MAKE_PLAYLIST_TITLE"].update("Songs found:")
                sendingSongs = []
                count = 1
                for song in songsresult:
                    if count > 5:
                        break
                    sendingSongs.append(song[0])
                    SongInfoText="Title: "+ song[2]+"\n"
                    artists = function1_1(song[0])
                    if not artists:
                        SongInfoText += "No Artist Info"
                    else:
                        SongInfoText += "Artists: "
                        artistText=""
                        for artist in artists:
                            artistText+=artist[1]+" "
                        SongInfoText+=artistText
                    window["MAKE_PLAYLIST_SONGINFO_"+str(count)].update(SongInfoText)
                    window["ADDPLAY_"+str(count)].update(visible=True)
                    window["ADDPLAY_"+str(count)].update(disabled=False)
                    count += 1
        window["-Songs_INPUT-"].update(value="")        
    
    if event.startswith("SearchSong2_"): 
        playlistId = event.split("_")[1]
        user_input = values["-Songs_INPUT-"]

        #Reset
        for i in range(1,6):
            window["MAKE_PLAYLIST_SONGINFO_"+str(i)].update("")
            window["ADDSONG_"+str(i)+"_"+playlistId].update(visible=False)
            window["ADDSONG_"+str(i)+"_"+playlistId].update(disabled=True)

        if not user_input.strip():
            sg.popup("Enter a song title!")
        else:
            songsresult = function1(user_input)
            if not songsresult:
                window["MAKE_PLAYLIST_TITLE"].update("NO Result of the song title")
            else: 
                window["MAKE_PLAYLIST_TITLE"].update("Songs found:")
                sendingSongs = []
                count = 1
                for song in songsresult:
                    if count > 5:
                        break
                    sendingSongs.append(song[0])
                    SongInfoText="Title: "+ song[2]+"\n"
                    artists = function1_1(song[0])
                    if not artists:
                        SongInfoText += "No Artist Info"
                    else:
                        SongInfoText += "Artists: "
                        artistText=""
                        for artist in artists:
                            artistText+=artist[1]+" "
                        SongInfoText+=artistText
                    window["MAKE_PLAYLIST_SONGINFO_"+str(count)].update(SongInfoText)
                    window["ADDSONG_"+str(count)+"_"+playlistId].update(visible=True)
                    window["ADDSONG_"+str(count)+"_"+playlistId].update(disabled=False)
                    count += 1
        window["-Songs_INPUT-"].update(value="")    

    if event.startswith("ADDSONG_"):
        songId = sendingSongs[int(event.split("_")[1])-1]
        playlist_Id = event.split("_")[2]
        result = function1_4(songId,playlist_Id)
        if result:
            sg.popup(result)
        else:
            sg.popup("Song Added")

    if event.startswith("PLAYLISTEN"):
        playlistId = event.split("_")[1]
        songId = event.split("_")[2]
        songTitle = event.split("_")[3]

        function6_2(songId)
        window.close()

        new_layout = create_listen_layout(playlistId)
        new_layout.insert(0,[[sg.Text("Playing"+songTitle)]])
        window = sg.Window("DEMO",new_layout,finalize=True)

        

    if event.startswith("ADDPLAY_"):
        songId = sendingSongs[int(event.split("_")[1])-1]
        window["MAKE_PLAYLIST_BUTTON"].update(visible=True)
        window["MAKE_PLAYLIST_BUTTON"].update(disabled=False)
        if songId in selectedSongs:
            sg.popup("It have already added")
        else:
            selectedSongs.append(songId)
            sg.popup("Song Added")

    
    if event == "MAKE_PLAYLIST_BUTTON":
        window.close()
        new_layout = create_main_playlist_confilm_layout()
        window = sg.Window("DEMO",new_layout)
    

    if event == "MAKE_PLAYLIST_BUTTON2":
        name_input = values["-Name_INPUT-"]
        desc_input = values["-Description_INPUT-"]

        if values["-Public-"]:
            sharing_input = 1
        elif values["-Private-"]:
            sharing_input = 0
        if not name_input:
            sg.popup("Playlist Name is required!")   
        else:
            function1_2(making_playlist_id,name_input,desc_input,sharing_input)
            function1_3(userId,making_playlist_id,1) #user is owner
            for song in selectedSongs:
                function1_4(song,making_playlist_id)

            sg.popup("You made playlist!")
            making_playlist_id = None
            selectedSongs = []
            sendingSongs = []

            go_main()


    if event == "SubScribe Playlist":
        window.close()
        new_layout = create_subscribe_playlist_layout()
        window = sg.Window("DEMO",new_layout)


    if event == "Search Playlist":
        user_input = values["-Subscribe_INPUT-"]

        #Reset
        for i in range(1,6):
            window["SUBSCRIBE_INFO_"+str(i)].update("")
            window["ADDMYPLAY_"+str(i)].update(visible=False)
            window["ADDMYPLAY_"+str(i)].update(disabled=True)

        if not user_input.strip():
            sg.popup("Enter a playlist title!")
        else:
            playlistsresult = function2(userId,user_input)
            if not playlistsresult:
                window["SUBSCRIBE_PLAYLIST_TITLE"].update("NO Result of the playlist title")
            else: 
                window["SUBSCRIBE_PLAYLIST_TITLE"].update("Playlists found:")
                layout_part =[sg.Text("Playlists found:")]
                sendingPlaylists = []
                count = 1
                for playlist in playlistsresult:
                    if count > 5:
                        break
                    sendingPlaylists.append(playlist[0])
                    playlistInfoText = "Name: "+playlist[1]+"\n"
                    if playlist[2]:
                        playlistInfoText += playlist[2]+"\n"
                    if playlist[4]:
                        playlistInfoText += "Official Playlist!\n"
                    if playlist[5]:
                        playlistInfoText += "Official Description: "+playlist[5]+"\n"
                    window["SUBSCRIBE_INFO_"+str(count)].update(playlistInfoText)
                    window["ADDMYPLAY_"+str(count)].update(visible=True)
                    window["ADDMYPLAY_"+str(count)].update(disabled=False)
                    count += 1

        window["-Subscribe_INPUT-"].update(value="")
    
    if event.startswith("ADDPMYPLAY_"):
        playlistId = sendingPlaylists[int(event.split("_")[1])-1]
        function1_3(userId, playlistId, 2)
        sg.popup("Playlist Added")

        go_main()

    if event == "Go To My Playlists":
        window.close()
        new_layout = create_my_playlists_layout()
        window = sg.Window("DEMO", new_layout)
        

    if event.startswith("ModifyPermission_"):
        playlistId = event.split("_")[1]
        playlistInfo = function5_1(playlistId)
        new_layout = create_modify_permission_layout(playlistId)
        window.close()
        window = sg.Window("DEMO", new_layout,finalize=True)
        window["-YOUR_PLAYLIST_NAME-"].update(playlistInfo[1])


    if event.startswith("SearchUser_"):
        playlistId = event.split("_")[1]
        user_input = values["-USERNAME_INPUT-"]

        for i in range(1,6):
            window["MP_"+str(i)].update("")
            window["ADDMP_"+{playlistId}+"_"+str(i)].update(visible=False)
            window["ADDMP_"+{playlistId}+"_"+str(i)].update(disabled=True)

        if not user_input.strip():
            sg.popup("Enter a user name!")
        else:
            playlistId = event.split("_")[1]
            usersresult = function3(user_input,playlistId)
            sendingUserName = []
            
            if not usersresult:
                layout_part = [sg.Text("NO Result of the playlist title")]
                window["MODIFY_PERMISSION_TITLE"].update("NO Result of the user")
            else: 
                window["MODIFY_PERMISSION_TITLE"].update("Users found:")
                count = 1
                for user in usersresult:
                    if count > 5:
                        break
                    window["MP_"+str(count)].update("Name: "+user[1])
                    sendingUserName.append(user[0])
                    count += 1

        window["-USERNAME_INPUT-"].update(value="")

    if event.startswith("ADDUSER_"):
        playlistId = event.split("_")[1]
        userId = sendingUserName[int(event.split("_")[2])-1]
        function1_3(userId, playlistId, 2)
        sg.popup("USER Added")

        sendingUserName = []
        go_main()

    if event.startswith("DELETEMPP_"):
        playlistId = event.split("_")[1]
        songId = event.split("_")[2]
        result = function5_3(playlistId,songId)
        if result:
            sg.popup(result)
        else:
            sg.popup("Deleted")
        window.write_event_value("ModifySongs_"+playlistId,None)
        
    if event.startswith("Listen_"):
        playlistId = event.split("_")[1]

        window.close()
        new_layout = create_listen_layout(playlistId)

        window = sg.Window("DEMO",new_layout,finalize=True)

    if event.startswith("ModifySongs_"):
        playlistId = event.split("_")[1]
        new_layout = create_modify_playlist_layout(playlistId)
        window.close()
        window = sg.Window("DEMO", new_layout,finalize=True)
        playlistInfo = function5_1(playlistId)
        window["-YOUR_PLAYLIST_NAME-"].update(playlistInfo[1])


    if event.startswith("ADDSONGMODIFY_"):
        playlistId = event.split("_")[1]
        new_layout = create_add_song_to_playlist_layout(playlistId)
        window.close()
        window = sg.Window("DEMO",new_layout)

        
    if event == sg.WIN_CLOSED:
        break

window.close()
mycursor.close()
mydb.close()