from django.contrib import admin

from .models import AuctionListing, AuctionCategory, User, AuctionBid, AuctionComment, Watchlist

class AuctionUserModel(admin.ModelAdmin):
    list_display = ("id", "username")

class AuctionListingModel(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid_price", "image_url", "category", "is_active", "created_on", "user")

class AuctionBidModel(admin.ModelAdmin):
    list_display = ("id", "current_bid_price", "user", "auction_listing_id", "created_on")

class AuctionCommentModel(admin.ModelAdmin):
    list_display = ("id", "listing", "comment", "user", "created_on")

class AuctionWatchlistModel(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "created_on")

# Register your models here.
admin.site.register(User, AuctionUserModel)
admin.site.register(AuctionListing, AuctionListingModel)
admin.site.register(AuctionCategory)
admin.site.register(AuctionBid, AuctionBidModel)
admin.site.register(AuctionComment, AuctionCommentModel)
admin.site.register(Watchlist, AuctionWatchlistModel)
