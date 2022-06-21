import threading
import time
import json
import requests

from .models import *
from django.db import transaction



URL = 'https://www.googleapis.com/youtube/v3/search?'
PARAMS = {
    'key': 'AIzaSyBt3R3dIeVQCXBmDmdeQ7c2YaTSa0L4zio',
    'part': 'snippet',
    'type': 'video',
    'order': 'date',
    'publishedAfter': '2022-06-21T00:00:00.00Z',
    'q': 'football'
}


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






def getYoutubeData(token = None):
    if token:
        PARAMS['pageToken'] = token
    
    response = requests.get(URL, PARAMS)
    
    if response.status_code == 200:
        youtubeDataFromApi = response.json()
        addYoutubeDataToDatabase(youtubeDataFromApi)
        return (True , youtubeDataFromApi['nextPageToken'])

    else:
        # handle error
        return (False , None)




def YoutubeApiCall():
    Run = True
    token = None
    while Run:
        print("Getting data from youtube API...") 
        Run , token = getYoutubeData(token)
        print("Youtube Data added to Database..")
        time.sleep(30)





def startThread():
    t = threading.Thread(target=YoutubeApiCall)
    t.daemon = True
    t.start() # this will run the `ping` function in a separate thread