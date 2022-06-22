from django.urls import path,include

from .views import *


urlpatterns = [
    path('videos' , YoutubeData.as_view() , name='video')
]
