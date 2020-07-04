#!/usr/bin/env python
# coding: utf-8


import pybase64
import requests
import datetime
from urllib.parse import urlencode
from collections import deque


class SpotifyAPI:
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'
    access_token_expires_in = datetime.datetime.now()
    token_did_expire = True
    access_token = None
    
    def __init__(self,client_id,client_secret): #*args,**kwargs
        self.client_id = client_id
        self.client_secret = client_secret

        
    def __get_client_creds_b64(self):
        if self.client_id==None or self.client_secret==None:
            raise Exception('client_id or client_secret not initialized')
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = pybase64.b64encode(client_creds.encode())
        #a byte object is required for base64 conversion and not str
        #encode() converts str into bytes and decode back to normal
        return client_creds_b64.decode()
    
    
    #provides token_data for authentication
    def __get_token_data(self): 
        return {
            'grant_type':'client_credentials'
        }
    
    
    #provides Basic type token_header for authentication
    def __get_token_header(self):  
        return {
            'Authorization':f'Basic {self.__get_client_creds_b64()}' #base64 needed
        }
        
        
    #performs authentication and gets access_token 
    def __authentication(self): 
        r = requests.post(self.token_url, data=self.__get_token_data(), headers=self.__get_token_header())
        accepted_token_response = r.json()
        if r.status_code not in range(200,206):
            raise Exception('Authentication Failed')
            #return False
        current_time = datetime.datetime.now()
        access_token = accepted_token_response['access_token']
        self.access_token = access_token
        expires_in = accepted_token_response['expires_in'] #in seconds
        self.access_token_expires_in = current_time + datetime.timedelta(seconds=expires_in)
        token_expired = self.access_token_expires_in
        self.token_did_expire = token_expired < current_time
        return True
    
    
    #checks if token is expired
    def __get_access_token(self):
        token = self.access_token
        token_expiration_time = self.access_token_expires_in
        current_time = datetime.datetime.now()
        if (token_expiration_time < current_time) or (token==None):
            self.__authentication()
            return self.__get_access_token()
        return token
    
    
    #provides header for api calls
    def __get_resource_header(self):
        access_token = self.__get_access_token()
        header = {
            'Authorization':f"Bearer {access_token}"
        }        
        return header
    
    
    #gets albums or artists using api calls, returns json file
    def __get_resource(self,lookup_id,resource='albums'):
        endpoint = f'https://api.spotify.com/v1/{resource}/{lookup_id}'
        header = self.__get_resource_header()
        r = requests.get(endpoint, headers=header)
        if r.status_code not in range(200,209):
            print('exit')
            return {}
        return r.json()
    
    
    #gives album info in the form of json file
    def get_album(self, album_id):
        return self.__get_resource(album_id,'albums')

    
    #gives artist info in the form of json file
    def get_artist(self, artist_id):
        return self.__get_resource(artist_id,'artists')
    
    
    #performs actual search query(api call), returns json file
    def __base_search(self,query):
        header = self.__get_resource_header()
        endpoint = 'https://api.spotify.com/v1/search'
        main_url = f"{endpoint}?{query}"
        r = requests.get(main_url,headers=header)
        r.json()
        if r.status_code not in range(200,206):
            return {}
        return r.json()
    
    
    #gets the query and search_type for search api call
    def search(self,query=None, search_type='track', operator=None, operator_query=None):
        if query==None:
            raise Exception('A query is required')
        if isinstance(query,dict):
                query = ' '.join([f"{key}:{value}" for key,value in query.items()])
        if operator!=None and operator_query!=None:
            if operator.lower() == 'or' or operator.lower() == 'not':
                operator = operator.upper()
                if isinstance(operator_query,str):
                    query = f"{query} {operator} {operator_query}"
        modified_query = urlencode({
            'q':query,
            'type':search_type.lower()
        })
        return self.__base_search(modified_query) 
    
    
    # extracts artist id from json
    def __get_id(self,artist_name):
        information = self.search(artist_name,'artist')
        return information['artists']['items'][0]['id']    
    
    
    #call function
    def get_tracks_of_artist(self,artist_name,country_code):
        artist_id = self.__get_id(artist_name)
        return self.__get_tracks(artist_id, country_code.upper())
    
    
    #performs api call to get an artists top songs 
    def __get_tracks(self,artist_id, ISO_3166_alpha_country_code):
        header = self.__get_resource_header()
        query = urlencode({
            'country': f'{ISO_3166_alpha_country_code}'
        })
        endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
        main_url = f'{endpoint}?{query}'
        r = requests.get(main_url, headers=header)
        if r.status_code not in range(200,206):
            return {}
        response = r.json()        
        return self.__extract_tracks(response) 
    
    
    #gets the name of tracks from json file, returns a list of items
    def __extract_tracks(self,response):
        tracks = deque()
        for i in response['tracks']:
            tracks.append(i['name'])
        return list(tracks)
    
    
    #call funtion
    def get_tracks_based_on_genres(self,genre='pop',artist=None):
        response = self.__find_tracks(genre,artist)
        return self.__extract_tracks(response)  
    
    
    #performs api call to find songs from provided genre, returns json
    def __find_tracks(self,genre,artist):
        genres = ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime","black-metal",
                  "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", 
                  "chicago-house", "children", "chill", "classical", "club", "comedy", "country", "dance",
                  "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", "disney",
                  "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", 
                  "french", "funk", "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge",
                  "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop",
                  "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial",
                  "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin",
                  "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno",
                  "movies","mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm",
                  "piano", "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", 
                  "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", "rock", 
                  "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes",
                  "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", "spanish", "study",
                  "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish",
                  "work-out", "world-music"]
        if genre not in genres:
            raise Exception('Tracks of provided genre are not available')
        if artist==None:
            query = urlencode({
                'seed_genres': f'{genre}'
            })
        else:
            artist_id = self.__get_id(artist)
            query = urlencode({
                'seed_artists': f'{artist_id}',
                'seed_genres': f'{genre}'
            })
        header = self.__get_resource_header()    
        endpoint = 'https://api.spotify.com/v1/recommendations'
        main_url = f'{endpoint}?{query}'
        r = requests.get(main_url, headers=header)
        if r.status_code not in range(200,206):
            return {}
        response = r.json()
        return response

