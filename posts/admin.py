from django.contrib import admin
from .models import Post, Comment, Like, PostHistory, Notifications
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostHistory)
admin.site.register(Notifications)