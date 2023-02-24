from django.db import models
from users.models import User
# Create your models here.


class Post(models.Model):
    image = models.ImageField(upload_to='posts', blank=True)
    caption = models.TextField(max_length=150)
    likes = models.ManyToManyField(User, related_name='postlikes', blank=True)
    post_created = models.DateTimeField(auto_now_add=True)
    post_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name='post', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-post_created']

    def __str__(self) -> str:
        return f"{self.user}'s post"

    def get_likes(self):
        return self.likes.all().count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        "Post", related_name="comments", on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    comment_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name="likedcomment", blank=True)
    reply = models.ForeignKey(
        "self", related_name="replies", blank=True, null=True, on_delete=models.CASCADE)
    isreply = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ['-comment_created']

    def __str__(self) -> str:
        return f"{self.user.username}'s comment"

    def get_likes(self):
        return self.likes.all()

    def save(self, *args, **kwargs):
        if self.reply:
            self.isreply = True
        return super().save(*args, **kwargs)
