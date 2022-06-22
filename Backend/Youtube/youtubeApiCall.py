import threading
import time
import json
import requests

from decouple import config

from .models import *
from django.db import transaction



URL = 'https://www.googleapis.com/youtube/v3/search?'
PARAMS = {
    'part': 'snippet',
    'type': 'video',
    'order': 'date',
    'publishedAfter': '2022-06-21T00:00:00.00Z',
    'q': 'football'
}


# Add data to the Database
def addYoutubeDataToDatabase(data):
    transaction.set_autocommit(False)
    
    try:
        pageInfoObj = PageInfo.objects.create(**{'totalResults' : data['pageInfo']['totalResults'] , 'resultsPerPage' : data['pageInfo']['resultsPerPage']})
        videoListObj = VideoList.objects.create(**{'kind' : data['kind'] , 'nextPageToken' : data['nextPageToken'] , 'pageInfo' : pageInfoObj})
    
        for item in data['items']:
            snippetObj = Snippet.objects.create(**{'publishedAt' : item['snippet']['publishedAt'] , 'title': item['snippet']['title'] , 'description': item['snippet']['description'], 'thumbnails': json.dumps(item['snippet']['thumbnails']), 'publishTime': item['snippet']['publishTime']})
            videoObj = Video.objects.create(**{'kind': item['kind'] , 'snippet': snippetObj, 'videoList': videoListObj})
    
    except:
        transaction.rollback()
        raise
    else:
        transaction.commit()
    finally:
        transaction.set_autocommit(True)





# Handling Youtube API GET request 
def getYoutubeData(key_list , key_index, token = None):
    if token:
        PARAMS['pageToken'] = token
    
    if key_index < len(key_list):
        PARAMS['key'] = key_list[key_index]
    else:
        return (False , 0 , None)
    
    response = requests.get(URL, PARAMS)
    
# Valid Response
    if response.status_code == 200:
        youtubeDataFromApi = response.json()
        addYoutubeDataToDatabase(youtubeDataFromApi)
        return (True , key_index , youtubeDataFromApi['nextPageToken'])

# Current API_KEY has exhausted its quota
    elif response.status_code == 403:
        return (True , key_index + 1, token)
    
# Handle Error
    else:
        return (False , 0 , None)




# Runs a continuous while loop to make GET request to Youtube API at an interval of 30 secs
def YoutubeApiCall():
    Run = True
    token = None
    key_index = 0
    key_list = config('YOUTUBE_DATA_KEY_LIST').split(',')
    while Run:
        print("Getting data from youtube API...") 
        
        Run , index , token = getYoutubeData(key_list, key_index, token)
        key_index = index

        print("Youtube Data added to Database..")
        time.sleep(30)




# Function to start a new thread for the Youtube API Call
def startThread():
    t = threading.Thread(target=YoutubeApiCall)
    t.daemon = True
    t.start() 