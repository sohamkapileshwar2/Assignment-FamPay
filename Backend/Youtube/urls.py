from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('AllUser' , views.UserViewSet, basename='AllUser')

urlpatterns = [
    path('videos' , YoutubeData.as_view() , name='video')
]
