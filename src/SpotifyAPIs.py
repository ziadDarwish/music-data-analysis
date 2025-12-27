import pylast
import pandas as pd
import requests
import json
import time
import numpy as np


def get_token():
    client_id = ''
    client_secret = ''
    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'client_credentials'
    }, auth=(client_id, client_secret))


    access_token = response.json()['access_token']
    return access_token

## Uncomment to get initial token

#token =  get_token()
#print(token)   

def fetch_web_api(endpoint, method='GET', body=None):
    global token
    url = f'https://api.spotify.com/{endpoint}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request(method, url, headers=headers, json=body)

    if response.status_code == 401:
        print('REAUTHENTICATING')
        response = requests.request(method, url, headers=headers, json=body)
    else:
     print(response.status_code)

    print(response)
    return response.json()




def get_album_info(id):
    endpoint = f'v1/albums/{id}'
    data = fetch_web_api(endpoint)
    pretty_json = json.dumps(data, indent=4)
    print(data['albums'][1])
    return data

def get_sevral_albums(albums_str):
    endpoint = f'v1/albums?ids={albums_str}'
    data = fetch_web_api(endpoint)
    # pretty_json = json.dumps(data, indent=4)
    # print(pretty_json)
    return data


def get_sevral_artists(artists_str):
    endpoint = f'v1/artists?ids={artists_str}'
    data = fetch_web_api(endpoint)
    return data


def get_artist_info(id):
    endpoint = f'v1/artists/{id}'
    data = fetch_web_api(endpoint)
    print(data)
    return data.get('items', [])



