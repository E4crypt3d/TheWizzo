from django.urls import path
from usertimeline import views


urlpatterns = [
    path("comment", views.add_comment, name="add-comment"),
    path("comment/like", views.like_comment, name="comment-like"),
    path("post/like", views.like_post, name="post-like"),
    path("post/comment/reply", views.reply_comment, name="reply-comment"),
]
