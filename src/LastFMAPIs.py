import pylast
import pandas as pd
import requests
import json
import time
import numpy as np



# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm

API_KEY = ""  
API_SECRET = ""

# In order to perform a write operation you need to authenticate yourself
username = ""
password_hash = pylast.md5("")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)


def get_lastfm_genres(artist_name):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'artist.getInfo',
        'artist': artist_name,
        'api_key': API_KEY,
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        tags = data['artist']['tags']['tag']
        genres = [tag['name'] for tag in tags]
        return ';'.join(genres) if genres else None
    except Exception:
        return None
    


def fill_missing_from_spotify(missing):
    try:
        for idx, row in missing.iterrows():
        
            artist_name = row['artist_name']  # or 'artist_name' — match your column
            genres = get_lastfm_genres(artist_name)
            print(idx,genres )
            if genres:
                missing.at[idx, 'genres'] = genres

    except Exception as e:
        print("Saving progress due to error...")
        missing.to_csv('artists_partial_genres.csv', index=False)
        raise e
