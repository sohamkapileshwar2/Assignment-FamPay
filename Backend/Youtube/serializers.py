from rest_framework import serializers

from .models import *


class PageInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageInfo
        fields = ('id' , 'totalResults' , 'resultsPerPage')


class VideoListSerializer(serializers.ModelSerializer):

    pageInfo = PageInfoSerializer()

    class Meta:
        model = VideoList
        fields = ('id' , 'kind' , 'nextPageToken', 'pageInfo')



class SnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snippet
        fields = ('id' , 'publishedAt' , 'title', 'description', 'thumbnails', 'publishTime')

    



class VideoSerializer(serializers.ModelSerializer):

    snippet = SnippetSerializer()

    class Meta:
        model = Video
        fields = ('id' , 'kind' , 'snippet', 'videoList')
