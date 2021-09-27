from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    body = models.TextField(default='')
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, null=True)


class PostLike(models.Model):
    user = models.ForeignKey(User, related_name="post_likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="liked_by", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_post_like"
            )
        ]


class Follow(models.Model):
    who = models.ForeignKey(User, related_name="who", on_delete=models.CASCADE)
    whom = models.ForeignKey(User, related_name="whom", on_delete=models.CASCADE)
