from django.contrib import admin
from .models import Post, Comment, Like, PostHistory
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostHistory)