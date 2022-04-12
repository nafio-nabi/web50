from django import forms
from .models import AuctionCategory


class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title", required=True, max_length=64, widget=forms.TextInput(attrs={"placeholder": "Enter title", "class": "form-control"}))
    description = forms.CharField(label="Description", required=True, max_length=192, widget=forms.Textarea(attrs={"placeholder": "Enter description", "class": "form-control", "rows": 5}))
    starting_bid_price = forms.DecimalField(label="Starting Bid Price", required=True, min_value=0.01, max_digits=7, decimal_places=2, widget=forms.NumberInput(attrs={"placeholder": "Enter starting bid price", "class": "form-control"}))
    image_url = forms.URLField(label="Image URL", required=False, widget=forms.URLInput(attrs={"placeholder": "Enter image URL", "class": "form-control"}))
    categories = AuctionCategory.objects.all()
    options = [(None, "Select a Category")]
    for category in categories:
        options.append((category.id, category.title))
    category = forms.ChoiceField(choices=options, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    user = forms.IntegerField(widget=forms.HiddenInput())

class BidForm(forms.Form):
    auction_listing = forms.IntegerField(widget=forms.HiddenInput())
    non_owner_bid_price = forms.DecimalField(label="Your Bid Price", max_digits=7, decimal_places=2, widget=forms.NumberInput(attrs={"placeholder": "Enter your bid price", "class": "form-control"}))
    user = forms.IntegerField(widget=forms.HiddenInput())

class WatchlistForm(forms.Form):
    listing = forms.IntegerField(widget=forms.HiddenInput())
    user = forms.IntegerField(widget=forms.HiddenInput())

class CloseListingForm(forms.Form):
    auction_listing = forms.IntegerField(widget=forms.HiddenInput())
    user = forms.IntegerField(widget=forms.HiddenInput())

class CommentForm(forms.Form):
    comment = forms.CharField(label="", required=False, max_length=256, widget=forms.Textarea(attrs={"placeholder": "Write your comment", "class": "form-control", "rows": 5}))
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    listing_id = forms.IntegerField(widget=forms.HiddenInput())