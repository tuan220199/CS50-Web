from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, related_name="owner")
    content = models.CharField(max_length=3000)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, null=True, related_name="user_like")

    def serialize_post(self):
        return {
            "id": self.id,
            "owner": self.owner.username,
            "likes": [user.username for user in self.likes.all()],
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        } 

    def __str__(self):
        return f"{self.owner} posts {self.content} at {timestamp}"

class Comment(models.Model):
    comment = models.CharField(max_length=3000, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="comment")
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")

    def serialize_comment(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "post_id": self.post.id,
            "user_comment": self.user_comment.username
        }

    def __str__(self):
        return f"{self.user_comment} comments {self.comment} on {self.post}"

class Follower(models.Model):
    followers = models.ManyToManyField(User, blank=True, null=True, related_name="followers")
    being_followered = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, related_name="being_followered") 

    def serialize_follow(self):
        return {
            "id": self.id,
            "follower": [user.username for user in self.followers.all()],
            "being_followered": self.being_followered.username,
        }
    