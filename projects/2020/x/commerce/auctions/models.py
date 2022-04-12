from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionCategory(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


# Auction listing
class AuctionListing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=640)
    starting_bid_price = models.DecimalField(max_digits=7, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(AuctionCategory, blank=True, null=True, on_delete=models.PROTECT, related_name="auction_category")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_listing")

    def __str__(self):
        return f"{self.title}"


#  Auction bid
class AuctionBid(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_listing_bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_listing_user")
    current_bid_price = models.DecimalField(max_digits=7, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user}, Bid amount: {self.current_bid_price}"


# Auction comment
class AuctionComment(models.Model):
    comment = models.TextField(max_length=256, blank=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_listing_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_comment_user")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user}, Comment: {self.comment}, Listing: {self.listing}"


class Watchlist(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user}, Watchlist item: {self.listing}"