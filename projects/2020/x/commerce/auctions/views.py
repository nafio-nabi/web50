from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import AuctionCategory, AuctionComment, AuctionListing, User, AuctionBid, Watchlist
from .forms import CreateListingForm, BidForm, CloseListingForm, CommentForm


def index(request):
    active_listings = AuctionListing.objects.filter(is_active=True).all()
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        create_listing_form = CreateListingForm(request.POST)
        if create_listing_form.is_valid():
            title = create_listing_form.cleaned_data["title"]
            description = create_listing_form.cleaned_data["description"]
            starting_bid_price = create_listing_form.cleaned_data["starting_bid_price"]
            image_url = create_listing_form.cleaned_data["image_url"]
            category = None
            if create_listing_form.cleaned_data["category"]:
                category = create_listing_form.cleaned_data["category"]
            category_id = category
            user_id = create_listing_form.cleaned_data["user"]
            listing = AuctionListing.objects.create(title=title, description=description, starting_bid_price=starting_bid_price, image_url=image_url, category_id=category_id, user_id=user_id)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Invalid submission"
            })
    create_listing_form = CreateListingForm(initial={"user": request.user.id})
    return render(request, "auctions/create_listing.html", {
        "create_listing_form": create_listing_form
    })


# @login_required
def listing(request, listing_id):
    non_user_bid_form = BidForm(initial={"user": request.user.id, "auction_listing": listing_id})
    comment_form = CommentForm(initial={"user_id": request.user.id, "listing_id": listing_id})
    listing = AuctionListing.objects.get(pk=listing_id)
    items = AuctionBid.objects.filter(auction_listing_id=listing).all()
    max_bid_price = items.aggregate(Max("current_bid_price"))
    bid_nums = len(items)
    logged_in_user = request.user.id
    listing_owner = listing.user.id
    
    if logged_in_user is not listing_owner:
        is_listing_owner = True
    else:
        is_listing_owner = False
    
    comments = AuctionComment.objects.filter(listing=listing_id).all
    
    if logged_in_user == listing_owner:
        close_listing_form = CloseListingForm(initial={"user": request.user.id, "auction_listing": listing_id})
    else:
        close_listing_form = None
    
    try:
        bidder = AuctionBid.objects.get(user=logged_in_user, auction_listing_id=listing_id)
    except:
        bidder = None

    winning_message = None
    if bidder:
        if bidder.is_winner:
            winning_message = "You have won this auction."
        

    try:
        in_watchlist = Watchlist.objects.get(user=request.user, listing=listing)
    except:
        in_watchlist = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "non_user_bid_form": non_user_bid_form,
        "comment_form": comment_form,
        "in_watchlist": in_watchlist,
        "max_bid_price": max_bid_price["current_bid_price__max"],
        "number_of_bids": bid_nums,
        "close_listing_form": close_listing_form,
        "logged_in_user": logged_in_user,
        "winning_message": winning_message,
        "comments": comments,
        "is_listing_owner": is_listing_owner
    })


def create_comment(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            listing_id = comment_form.cleaned_data["listing_id"]
            user_id = comment_form.cleaned_data["user_id"]
            comment = comment_form.cleaned_data["comment"]
            AuctionComment.objects.create(comment=comment, listing_id=listing_id, user_id=user_id)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def create_bid(request):
    if request.method == "POST":
        bid_form= BidForm(request.POST)
        if bid_form.is_valid():
            auction_listing = int(bid_form.cleaned_data["auction_listing"])
            current_bid_price = bid_form.cleaned_data["non_owner_bid_price"]
            user = bid_form.cleaned_data["user"]
            auction_listing_user = AuctionListing.objects.get(pk=auction_listing).user.id
            starting_bid_price = AuctionListing.objects.get(pk=auction_listing).starting_bid_price
            items = AuctionBid.objects.filter(auction_listing_id=auction_listing).all()
            max_bid_price = items.aggregate(Max("current_bid_price"))
            if current_bid_price >= starting_bid_price:
                if max_bid_price["current_bid_price__max"] is not None:
                    if current_bid_price > max_bid_price["current_bid_price__max"]:
                        AuctionBid.objects.create(auction_listing_id=auction_listing, user_id=user, current_bid_price=current_bid_price)
                        max_bid_price = items.aggregate(Max("current_bid_price"))
                        bid_nums = len(items)
                        if user is not auction_listing_user:
                            is_listing_owner = True
                        else:
                            is_listing_owner = False
                        return render(request, "auctions/listing.html", {
                            "success_message": f"Your bid price of ${current_bid_price} was successfully submitted.",
                            "listing": AuctionListing.objects.get(pk=auction_listing),
                            "non_user_bid_form": BidForm(initial={"user": request.user.id, "auction_listing": auction_listing}),
                            "max_bid_price": max_bid_price["current_bid_price__max"],
                            "number_of_bids": bid_nums,
                            "is_listing_owner": is_listing_owner
                        })
                    else:
                        max_bid_price = items.aggregate(Max("current_bid_price"))
                        bid_nums = len(items)
                        if user is not auction_listing_user:
                            is_listing_owner = True
                        else:
                            is_listing_owner = False
                        return render(request, "auctions/listing.html", {
                            "message": f"Error: Your bid price must be greater than ${max_bid_price['current_bid_price__max']}",
                            "listing": AuctionListing.objects.get(pk=auction_listing),
                            "non_user_bid_form": BidForm(initial={"user": request.user.id, "auction_listing": auction_listing}),
                            "max_bid_price": max_bid_price["current_bid_price__max"],
                            "number_of_bids": bid_nums,
                            "is_listing_owner": is_listing_owner
                        })
                else:
                    AuctionBid.objects.create(auction_listing_id=auction_listing, user_id=user, current_bid_price=current_bid_price)
                    max_bid_price = items.aggregate(Max("current_bid_price"))
                    bid_nums = len(items)
                    if user is not auction_listing_user:
                        is_listing_owner = True
                    else:
                        is_listing_owner = False
                    return render(request, "auctions/listing.html", {
                        "success_message": f"Your bid price of ${current_bid_price} was successfully submitted.",
                        "listing": AuctionListing.objects.get(pk=auction_listing),
                        "non_user_bid_form": BidForm(initial={"user": request.user.id, "auction_listing": auction_listing}),
                        "max_bid_price": max_bid_price["current_bid_price__max"],
                        "number_of_bids": bid_nums,
                        "is_listing_owner": is_listing_owner
                    })
            else:
                max_bid_price = items.aggregate(Max("current_bid_price"))
                bid_nums = len(items)
                if user is not auction_listing_user:
                    is_listing_owner = True
                else:
                    is_listing_owner = False
                return render(request, "auctions/listing.html", {
                    "message": f"Error: Your bid price must be at least ${starting_bid_price}",
                    "listing": AuctionListing.objects.get(pk=auction_listing),
                    "non_user_bid_form": BidForm(initial={"user": request.user.id, "auction_listing": auction_listing}),
                    "max_bid_price": max_bid_price["current_bid_price__max"],
                    "number_of_bids": bid_nums,
                    "is_listing_owner": is_listing_owner
                })
        else:
            if user is not auction_listing_user:
                is_listing_owner = True
            else:
                is_listing_owner = False
            return render(request, "auctions/listing.html", {
                    "message": f"Error: Invalid",
                    "listing": AuctionListing.objects.get(pk=auction_listing),
                    "non_user_bid_form": BidForm(initial={"user": request.user.id, "auction_listing": auction_listing}),
                    "is_listing_owner": is_listing_owner
                })


def close_listing(request):
    if request.method == "POST":
        close_listing_form = CloseListingForm(request.POST)
        if close_listing_form.is_valid():
            listing_id = close_listing_form.cleaned_data["auction_listing"]
            user_id = close_listing_form.cleaned_data["user"]
            # Get all records of the AuctionBid of the listing
            bid_listings = AuctionBid.objects.filter(auction_listing_id=listing_id).all()
            if len(bid_listings):
                # Get record of highest bid
                highest_bid = bid_listings.last()
                # Set highest bidder to true
                highest_bid.is_winner = True
                highest_bid.save()
                # Deactivate listing
                listing = AuctionListing.objects.get(pk=listing_id)
                listing.is_active = False
                listing.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                # If no bids on listing then Deactivate listing
                listing = AuctionListing.objects.get(pk=listing_id)
                listing.is_active = False
                listing.save()
                return HttpResponseRedirect(reverse("index"))

@login_required
def watchlist(request):
    if request.method == "POST":
        listing = request.POST["listing"]
        user = request.POST["user"]
        try:
            in_watchlist = Watchlist.objects.get(user=user, listing=listing)
        except:
            in_watchlist = None

        if in_watchlist:
            Watchlist.objects.filter(user=user, listing=listing).delete()
        else:
            Watchlist.objects.create(listing_id=listing, user_id=user)
        return HttpResponseRedirect(reverse("listing", args=(listing,)))
    watchlist = Watchlist.objects.filter(user=request.user).all()
    listings = []
    for listing in watchlist:
        listings.append(AuctionListing.objects.get(title=listing.listing.title))
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def categories(request):
    categories = AuctionCategory.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listing(request, category_id):
    category = AuctionCategory.objects.get(pk=category_id)
    category_listings = category.auction_category.filter(is_active=True).all()
    return render(request, "auctions/categories_listing.html", {
        "category": category,
        "category_listings": category_listings
    })