from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *

from .youtubeApiCall import startThread

import sys



# Starting Youtube API Call thread when server is running
if 'runserver' in sys.argv:
    startThread()


# Pagination enabled for displaying the video data stored in database
class YoutubeDataPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


# Handling GET request at /youtube-api/videos
class YoutubeData(generics.ListAPIView):
    queryset = Video.objects.all().order_by('-snippet__publishedAt') # Queryset is already ordered by publishedAt attribute in descending order
    serializer_class = VideoSerializer
    pagination_class = YoutubeDataPagination

    
    # Handling Filtering functionality based on title and description specified in query params
    # Note - Each word seperated by a space in title or description is checked for a match in the respective fields
    def filter_queryset(self, queryset):

        title = self.request.GET.get('title' , None)
        description = self.request.GET.get('description' , None)
        
        if title:
            title_words = title.split()
            Q_obj = Q()
            for word in title_words:
                Q_obj = Q_obj | Q(snippet__title__icontains=word)
            queryset = queryset.filter(Q_obj)
        
        if description:
            description_words = description.split()
            Q_obj = Q()
            for word in description_words:
                Q_obj = Q_obj | Q(snippet__description__icontains=word)
            queryset = queryset.filter(Q_obj)

        
        return queryset










