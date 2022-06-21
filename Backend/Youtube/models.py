from django.db import models


# Create your models here.


class PageInfo(models.Model):

    totalResults = models.IntegerField()
    resultsPerPage = models.IntegerField()



class VideoList(models.Model):

    kind = models.CharField(max_length=40)
    nextPageToken = models.CharField(max_length=20)
    pageInfo = models.OneToOneField(PageInfo, on_delete=models.SET_NULL , null=True)



class Snippet(models.Model):

    publishedAt = models.CharField(max_length=40)
    title = models.TextField()
    description = models.TextField()
    thumbnails = models.JSONField()
    publishTime = models.CharField(max_length=40)



class Video(models.Model):

    kind = models.CharField(max_length=40)
    snippet = models.OneToOneField(Snippet, on_delete=models.CASCADE , related_name='video')
    videoList = models.ForeignKey(VideoList , on_delete=models.CASCADE , related_name='video')
    
