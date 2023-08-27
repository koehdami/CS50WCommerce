from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, unique=True)
    pass

class Auctions(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.CharField(max_length=128, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    open = models.BooleanField()
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="winner")
    def __str__(self):
        return f"Auction_id: {self.id}, Auction title: '{self.title}', Price: {self.price}"

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    auctions_id = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="bids")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.user_id.username} bid {self.bid}$ on {self.auctions_id.title} (Auctions_id: {self.auctions_id.id})"

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    auctions_id = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="comments")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user_id}: wrote '{self.comment}'  (Auctions_id: {self.auctions_id.id})"
    

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Users_Watchlist")
    auctions_id = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="Active_Watchers")

    def __str__(self):
        return f"{self.user_id.username} is watching (Auctions_id: {self.auctions_id.id})"