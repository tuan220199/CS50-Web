from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # already have username, email and password
    pass

class Category(models.Model):
    group = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.group}" 

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=3000)
    image = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)    
    initial_price = models.FloatField()
    
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    comment = models.CharField(max_length=3000, null=True)
    listing_comment = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="listing_comment")
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_comment")

    def __str__(self):
        return f"{self.user_comment} comments: {self.comment} on {self.listing_comment}"

class Bid(models.Model):
    bid = models.FloatField(null=True)
    listing_bid = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="listing_bid")
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_bid")

    def __str__(self):
        return f"{self.user_bid} bids: {self.bid} on {self.listing_bid}"

class Watch_list(models.Model):
    user_watch_list = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True, related_name="user_watch_list")
    list_watch = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank= True, related_name="list_watch")