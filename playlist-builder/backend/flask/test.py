from flask import Flask, request, json
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import json

CL_ID = "id"
CL_SECRET = "secret"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CL_ID,
                                            client_secret=CL_SECRET,
                                            redirect_uri="http://localhost:8080",
                                            scope="playlist-modify-private"))

username = sp.current_user()["id"]

app = Flask(__name__)
data = []

# Functions to help with processing --------------------
def getSong(sName, aName):
    count = -1
    sName_res = sp.search(q=(sName + ' ' + aName), limit=10, type="track")
    for idx, track in enumerate(sName_res['tracks']['items']):
        #print(idx, ":", track['name'], "by", track['artists'][0]['name'], track['uri'])
        count += 1

    song_sel = 0

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
    recs = sp.recommendations(seed_tracks={uri}, limit=20)
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
    recs = sp.recommendations(seed_tracks={uri}, limit=30)
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

# ---------------------------------------------------------------------------------------------------------------------------------------
@app.route('/getData', methods=['POST'])
def main():
    #------------------------------------------------------------------------------------------
    # The "Main" function of the program 
    data = request.get_data(as_text=True)
    d = json.loads(data)

    print(d)

    # Playlist Builder:
    #playlist_info = getInfo("filename") # Read in a file to process the form from the frontend
    init_uri = getSong(d["songName"], d["artistName"])                # Get the uri of the song the user searches for
    uri_list = [init_uri]               # Create the initial list to populate

    # Populate the list of URIs
    uri_list = getRecommended(uri_lst=uri_list, increases=d['tempo'], size=d['length'])

    # Create the playlist itself
    playlist = sp.user_playlist_create(username, d['playlistName'], public=False, collaborative=False, description="") 
    sp.user_playlist_add_tracks(username, playlist['uri'], uri_list, position=None) # Add the songs from the URI list to the playlist

    # Et Voila!
    return data