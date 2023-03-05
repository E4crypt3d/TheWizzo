from django.contrib import admin
from .models import Post, Comment
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_created', 'post_updated', 'caption']
    list_display_links = ['user', 'post_created', 'post_updated', 'caption']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'reply']
    list_display_links = ['user', 'post', 'comment', 'reply']
