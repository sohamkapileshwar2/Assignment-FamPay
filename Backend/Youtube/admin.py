from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(VideoList)
admin.site.register(PageInfo)

admin.site.register(Video)
admin.site.register(Snippet)