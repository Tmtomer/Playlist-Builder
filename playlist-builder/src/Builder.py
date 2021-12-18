import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
CL_ID = "Enter the client id here"
CL_SECRET = "Enter the client secret here"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CL_ID,
                                               client_secret=CL_SECRET,
                                               redirect_uri="http://localhost:8080",
                                               scope="playlist-modify-private"))

username = sp.current_user()["id"]

def getSong():
    count = -1
    sName = input("\nEnter the name of the song for the playlist\n")
    sName_res = sp.search(q=sName, limit=10, type="track")
    for idx, track in enumerate(sName_res['tracks']['items']):
        print(idx, ":", track['name'], "by", track['artists'][0]['name'], track['uri'])
        count += 1

    song_sel = -1
    while True:
        try:
            print("Select the index of the song you want to make the playlist from, and then press enter.")
            song_sel = int(input())
            if song_sel not in range(0,count+1):
                raise ValueError
        except ValueError:
            print("Please enter a valid index.")
        else:
            break

    s_uri = ''
    for idx, track in enumerate(sName_res['tracks']['items']):
        if idx == song_sel:
            s_uri = track['uri']

    return s_uri

def getRecommended(uri_lst, increases, size):
    count = 0
    while count < size:
        count += 1
        if not uri_lst:
            break
        else:
            temp = uri_lst.pop() # Get the most recent value stored in a variable
            uri_lst.append(temp) # Add it back in

            if increases:
                next_song = getRecommended_higher(temp)
            else:
                next_song = getRecommended_lower(temp)
            if next_song == -1:
                break
            else:
                uri_lst.append(next_song) # Get the next recommended song and add it to the list

    iter = 0
    while iter < len(uri_lst):
        uri_lst[iter] = uri_lst[iter].replace("spotify:track:", "")
        iter += 1
    
    return uri_lst

def getRecommended_lower(uri):
    init_data = sp.audio_analysis(uri)
    init_tempo = init_data['track']['tempo']
    rec_data = ''
    recs = sp.recommendations(seed_tracks={init_uri}, limit=20)
    tempo_list = []
    for idx, track in enumerate(recs['tracks']):
        rec_data = sp.audio_analysis(track['uri'])   # Store the audio analysis data
        if(rec_data['track']['tempo'] < init_tempo): # Only look to add the songs with a lower tempo than the provided song
            tempo_list.append(rec_data['track']['tempo'])

    tempo_list.sort()
    if not tempo_list:
        return -1
    else:
        next_song_tempo = tempo_list.pop()
        next_song_uri = ''
        for idx, track in enumerate(recs['tracks']):
            tmp_tempo = sp.audio_analysis(track['uri'])
            if(tmp_tempo['track']['tempo'] == next_song_tempo):
                next_song_uri = track['uri']
                break

        return next_song_uri

def getRecommended_higher(uri):
    init_data = sp.audio_analysis(uri)
    init_tempo = init_data['track']['tempo']
    rec_data = ''
    recs = sp.recommendations(seed_tracks={init_uri}, limit=30)
    tempo_list = []
    for idx, track in enumerate(recs['tracks']):
        rec_data = sp.audio_analysis(track['uri'])   # Store the audio analysis data
        if(rec_data['track']['tempo'] > init_tempo): # Only look to add the songs with a lower tempo than the provided song
            tempo_list.append(rec_data['track']['tempo'])

    tempo_list.sort(reverse=True)
    if not tempo_list:
        return -1
    else:
        next_song_tempo = tempo_list.pop()
        next_song_uri = ''
        for idx, track in enumerate(recs['tracks']):
            tmp_tempo = sp.audio_analysis(track['uri'])
            if(tmp_tempo['track']['tempo'] == next_song_tempo):
                next_song_uri = track['uri']
                break
    
        return next_song_uri
#``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
def getInfo(fname):
    # This function needs to read some kind of input file and gather the following data
    # 1. The name of the playlist
    # 2. Whether or not the tempo is increasing or decreasing
    #       Increasing -> True
    #       Decreasing -> False
    # 3. Length of playlist (a.k.a the number of songs)
    #
    # The file should have this format for now
    data = ["My Generated Playlist", False, 15] #THIS IS TEMPORARY USER INPUT, THIS FUNCTION SHOULD PROCESS THE FILE TO GET THE INFO
    return data
#`````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

#------------------------------------------------------------------------------------------
# The "Main" function of the program 
playlist_info = getInfo("filename") # Read in a file to process the form from the frontend
init_uri = getSong()                # Get the uri of the song the user searches for
uri_list = [init_uri]               # Create the initial list to populate

# Populate the list of URIs
uri_list = getRecommended(uri_lst=uri_list, increases=False, size= playlist_info[2])

# Create the playlist itself
playlist = sp.user_playlist_create(username, playlist_info[0], public=False, collaborative=False, description="") 

sp.user_playlist_add_tracks(username, playlist['uri'], uri_list, position=None) # Add the songs from the URI list to the playlist

# Et Voila!