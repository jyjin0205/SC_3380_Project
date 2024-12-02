import mysql.connector
import PySimpleGUI as sg
import uuid

####### global variable #########
making_playlist_id = None
userId = "user1"
selectedSongs = []

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
    
    query = "INSERT INTO PLAYLISTMUSIC (Playlist_id,Music_id) VALUES(%s, %s)"
    mycursor.execute(query,(playlistId,musicId,))
    mydb.commit()


#Func2 : User_Subscribe_the_playlist
def function2(userId, playlistName):
    query = """
        SELECT * FROM PLAYLIST p 
        WHERE p.Sharing_type==1 
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



##########layout part##########
# Main Window
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

# Func1 : Make Playlist Window
make_playlist_layout = [
    [sg.Text("Insert Songs")],
    [sg.In(key="-Songs_INPUT-"), sg.Button("Search Song")],
    [sg.Column([], key="-RESULT_LAYOUT-", scrollable=True, vertical_scroll_only=True, size=(400, 200))],
    [sg.Button("Confilm", key="MAKE_PLAYLIST_BUTTON", disabled=True, visible=False)]
]

make_playlist_confilm_layout = [
    [sg.Text("Insert Playlist's Name:")],
    [sg.In(key="-Name_INPUT-")],
    [sg.Text("Insert Description:")],
    [sg.In(key="-Description_INPUT-")],
    [sg.Text("Choose Sharing Type")],
    [sg.Radio("Public", "RADIO_GROUP", key="-Public-",default=True)],
    [sg.Radio("Private", "RADIO_GROUP", key="-Privaate-")],
    [sg.Button("Confilm", key="MAKE_PLAYLIST_BUTTON2")]
]

# Func2 : Subscribe Playlist Window
subscribe_playlist_layout = [
    [sg.Text("Subscribe")],
    [sg.In(key="-Subscribe_INPUT-"),sg.Button("Search Playlist")],
    [sg.Column([], key="-RESULT_LAYOUT-", scrollable=True, vertical_scroll_only=True, size=(400, 200))],
]

# Func3 & 4 & 5 : My Playlists Window
my_playlists_layout = [
    [sg.Text("Your")],
    [sg.Text("",key="-YOUR_PLAYLIST_NAME-")],
    [sg.Column([], key="-MODIFY_RESULT_LAYOUT-", scrollable=True)]
]

# Func3 : Modify Permission Window
default_modify_permission_layout = [
    [sg.Text("Your")],
    [sg.Text("",key="-YOUR_PLAYLIST_NAME-")],
    [sg.In(key="-USERNAME_INPUT-")],
    [sg.Column([], key="-MODIFY_RESULT_LAYOUT-", scrollable=True)]
]

modify_permission_layout = default_modify_permission_layout

# Func4 : Modify Playlist Window
modify_playlist_layout = [
    [sg.Text("Your")],
    [sg.Text("",key="-YOUR_PLAYLIST_NAME-")],
    [sg.Column([], key="-MODIFY_PLAYLIST_LAYOUT-", scrollable=True)]
]

add_song_layout = [
    [sg.Text("Enter Song Name")],
    [sg.In(key="-Songs_INPUT-")]
]

###### GUI Function #######

def go_main():
    return "GO_MAIN"

def create_main_btn(layout):
    layout.append([sg.Button("Main")])
    return layout

##########GUI Part#########

# Create the window
window = sg.Window("DEMO", main_layout)
current_layout = main_layout


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "GO_MAIN" or event == "Main":
        window.close()
        window = sg.Window("DEMO", main_layout)
        current_layout = main_layout

    if event == "Make Playlist":
        making_playlist_id = str(uuid.uuid4())
        window.close()
        window = sg.Window("DEMO", make_playlist_layout)
        current_layout = make_playlist_layout
    
    #Make_Playlist_layout
    if event == "Search Song" and current_layout == make_playlist_layout :
        user_input = values["-Songs_INPUT-"]
        window["-RESULT_LAYOUT-"].update([]) ## reset result

        if not user_input.strip():
            sg.popup("Enter a song title!")
        else:
            songsresult = function1(user_input)
            if not songsresult:
                layout_part = [sg.Text("NO Result of the song title")]
                window.extend_layout(window["-RESULT_LAYOUT-"],[layout_part])
            else: 
                layout_part = []
                layout_part.append([sg.Text("Songs found:")])

                for song in songsresult:
                    layout_part_part = []
                    layout_part_part.append(sg.Text("Title: "+song[2])) 
                    artists = function1_1(song[0])
                    if not artists:
                        layout_part_part.append(sg.Text("No Artist Info"))
                    else:
                        layout_part_part.append(sg.Text("Artists:"))
                        for artist in artists:
                            layout_part_part.append(sg.Text(artist[1]))
                    layout_part_part.append(sg.Button("Add to Playlist",key=f"ADDPLAY_{song[0]}"))
                    layout_part.append(layout_part_part)

                window.extend_layout(window["-RESULT_LAYOUT-"], layout_part)
        window["-Songs_INPUT-"].update(value="")

    if event.startswith("SearchSong_"): 
        playlistId = event.split("_")[1]
        user_input = values["-Songs_INPUT-"]
        if not user_input.strip():
            sg.popup("Enter a song title!")
        else:
            songsresult = function1(user_input)
            if not songsresult:
                layout_part = [sg.Text("NO Result of the song title")]
                window.extend_layout(window["-RESULT_LAYOUT-"],[layout_part])
            else: 
                window["-RESULT_LAYOUT-"].update([])
                layout_part =[sg.Text("Songs found:")]
                for song in songsresult:
                    layout_part.append(sg.Text("Title: "+song[2])) 
                    artists = function1_1(song[0])
                    if not artists:
                        layout_part.append(sg.Text("No Artist Info"))
                    else:
                        layout_part.append(sg.Text("Artists:"))
                        for artist in artists:
                            layout_part.append(sg.Text(artist[1]))
                    layout_part.append(sg.Button("Add to Playlist",key=f"ADDPLAY2_{song[0]}_{playlistId}"))
                print(layout_part)
                window.extend_layout(window["-RESULT_LAYOUT-"], [layout_part])
        window["-Songs_INPUT-"].update(value="")        
    

    if event.startswith("ADDPLAY_"):
        songId = event.split("_")[1]
        window["-MAKE_PLAYLIST_BUTTON"].update(visible=True)
        window["-MAKE_PLAYLIST_BUTTON"].update(disabled=False)
        selectedSongs.append(songId)
        sg.popup("Song Added")
        window["-RESULT_LAYOUT-"].update([])


    if event.startswith("ADDPLAY2_"):
        songId = event.split("_")[1]
        playlist_Id = event.split("_")[2]
        function1_4(songId,playlist_Id)
        sg.popup("Song Added")
        window["-RESULT_LAYOUT-"].update([])

    
    if event == "MAKE_PLAYLIST_BUTTON":
        window["-RESULT_LAYOUT-"].update([]) ## reset to confilm

        window.close()
        window = sg.Window("DEMO",make_playlist_confilm_layout)
        current_layout = make_playlist_confilm_layout
    

    if event == "MAKE_PLAYLIST_BUTTON2":
        name_input = values["-Name_INPUT-"]
        desc_input = values["-Description_INPUT-"]

        if values["-Public-"]:
            sharing_input = 1
        elif values["-Private-"]:
            sharing_input = 0
        if not name_input:
            sg.pop("Playlist Name is required!")   
        else:
            function1_2(making_playlist_id,name_input,desc_input,sharing_input)
            function1_3(userId,making_playlist_id,1) #user is owner
            for song in selectedSongs:
                function1_4(song,making_playlist_id)

            sg.pop("You made playlist!")
            making_playlist_id = None
            selectedSongs = []

            go_main()


    if event == "SubScribe Playlist":
        window.close()
        window = sg.Window("DEMO", subscribe_playlist_layout)
        current_layout = subscribe_playlist_layout


    if event == "Search Playlist":
        user_input = values["-Subscribe_INPUT-"]
        if not user_input.strip():
            sg.popup("Enter a playlist title!")
        else:
            playlistsresult = function2(userId,user_input)
            if not playlistsresult:
                layout_part = [sg.Text("NO Result of the playlist title")]
                window.extend_layout(window["-RESULT_LAYOUT-"],[layout_part])
            else: 
                window["-RESULT_LAYOUT-"].update([])
                layout_part =[sg.Text("Playlists found:")]
                for playlist in playlistsresult:
                    layout_part.append(sg.Text("Name: "+playlist[1])) 
                    if playlist[2]:
                        layout_part.append(playlist[2])
                    
                    if playlist[4]:
                        layout_part.append("Official Playlist!")

                    if playlist[5]:
                        layout_part.append("Official Description: "+playlist[5])
                    
                    layout_part.append(sg.Button("Add to My Playlist",key=f"ADDMYPLAY_{playlist[0]}"))

                window.extend_layout(window["-RESULT_LAYOUT-"], [layout_part])
        window["-Subscribe_INPUT-"].update(value="")
    
    if event.startswith("ADDPMYPLAY_"):
        playlistId = event.split("_")[1]
        function1_3(userId, playlistId, 2)
        sg.popup("Playlist Added")
        window["-RESULT_LAYOUT-"].update([])

        go_main()

    if event == "Go To My Playlists":
        myresult = function5(userId)
        for playlistId in myresult:
            playlistInfo = function5_1(playlistId)
            OwningStatus = function5_2(userId,playlistId)
            layout_part = [sg.Text("Playlist's Name: "+ playlistInfo[1]),
                           sg.Text(playlistInfo[2]),
                           sg.Text("Public Playlist") if playlistInfo[3] else sg.Text("Private Playlist"),
                           sg.Text("Owner") if OwningStatus[0] == 1 else sg.Text("Subscriber")
                           ]
            
            #If user is owner
            if OwningStatus[0] == 1:
                if playlistInfo[3] == 0:
                    layout_part.append(sg.Button("Modify Permission",key=f"ModifyPermission_{playlistId}"))
            
            #If user can modify it
            if OwningStatus[0] == 1 or OwningStatus[0] == 2 :
                layout_part.append(sg.Button("Modify Songs",key=f"ModifySongs_{playlistId}"))
            my_playlists_layout.append(layout_part)


        window = sg.Window("DEMO", my_playlists_layout)
        current_layout = my_playlists_layout
        

    if event.startswith("ModifyPermission_"):
        playlistId = event.split("_")[1]
        playlistInfo = function5_1(playlistId)

        modify_permission_layout.append(sg.Button("Search User",key=f"SearchUser_{playlistId}"))
        modify_permission_layout.append([sg.Column([], key="-MODIFY_RESULT_LAYOUT-", scrollable=True)])
        window.close()
        window = sg.Window("DEMO", modify_permission_layout)
        current_layout = modify_permission_layout

 
        window["-YOUR_PLAYLIST_NAME-"].update(playlistInfo[1])
        sg.Button("Search UserName")


    if event.startswith("SearchUser_"):
        user_input = values["-USERNAME_INPUT-"]
        if not user_input.strip():
            sg.popup("Enter a user name!")
        else:
            playlistId = event.split("_")[1]
            usersresult = function3(user_input,playlistId)
            if not usersresult:
                layout_part = [sg.Text("NO Result of the playlist title")]
                window.extend_layout(window["-MODIFY_RESULT_LAYOUT-"],[layout_part])
            else: 
                window["-MODIFY_RESULT_LAYOUT-"].update([])
                layout_part =[sg.Text("Users found:")]
                for user in usersresult:
                    layout_part.append(sg.Text("Name: "+user[1])) 
                    layout_part.append(sg.Button("Add User",key=f"ADDUSER_{playlistId}_{user[0]}"))

                window.extend_layout(window["-MODIFY_RESULT_LAYOUT-"], [layout_part])
        window["-USERNAME_INPUT-"].update(value="")

    if event.startswith("ADDUSER_"):
        playlistId = event.split("_")[1]
        userId = event.split("_")[2]
        function1_3(userId, playlistId, 2)
        sg.popup("USER Added")

        modify_permission_layout = default_modify_permission_layout
        go_main()


    if event.startswith("ModifySongs_"):
        playlistId = event.split("_")[1]
        modify_playlist_layout.append([sg.Button("Add Songs",key=f"ADDSONG_{playlistId}"),sg.Button("Go Main")])
        window.close()
        window = sg.Window("DEMO", modify_playlist_layout)
        current_layout = modify_playlist_layout

        playlistInfo = function5_1(playlistId)
        window["-YOUR_PLAYLIST_NAME-"].update(playlistInfo[1])

        #song 띄워줘야 함
        songsInfo = function4(playlistId)
        if not songsInfo:
            layout_part = [sg.Text("NO Result of the song")]
            window.extend_layout(window["-MODIFY_PLAYLIST_LAYOUT-"],[layout_part])
        else: 
            window["-MODIFY_PLAYLIST_LAYOUT-"].update([])
            layout_part=[]
            for song in songsInfo:
                layout_part.append(sg.Text("Title: "+song[2])) 
                artists = function1_1(song[0])
                if not artists:
                    layout_part.append(sg.Text("No Artist Info"))
                else:
                    layout_part.append(sg.Text("Artists:"))
                    for artist in artists:
                        layout_part.append(sg.Text(artist[1]))
                layout_part.append(sg.Button("DELETE",key=f"DELETEPLAY_{song[0]}"))
            window.extend_layout(window["-MODIFY_PLAYLIST_LAYOUT-"], [layout_part])        


    if event.startswith("ADDSONG_"):
        playlistId = event.split("_")[1]
        add_song_layout.append(sg.Button("Search Songs",key=f"SearchSong_{playlistId}"))
        add_song_layout.append(sg.Button("Go To Playlist",key=f"GOTOPLAYLIST_{playlistId}"))
        add_song_layout.append([sg.Column([], key="-MODIFY_RESULT_LAYOUT-", scrollable=True)])


    if event == sg.WIN_CLOSED:
        break

window.close()
mycursor.close()
mydb.close()