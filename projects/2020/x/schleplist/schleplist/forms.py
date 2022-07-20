from django import forms
from .models import User

class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=True, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', required=True, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class SignInForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class NewPostForm(forms.Form):
    title = forms.CharField(label='Title', required=True, min_length=15, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Write a title for your schlep', 'class': 'form-control'}))
    body = forms.CharField(label='Body', required=True, min_length=75, max_length=640, widget=forms.Textarea(attrs={'placeholder': 'Describe your schlep in detail', 'class': 'form-control', 'rows': '6'}))


class ImageUploadForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=False, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', required=False, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    profile_image = forms.ImageField(label='Profile Image', required=False)


class BookmarkForm(forms.Form):
    post = forms.IntegerField(required=False, widget=forms.HiddenInput())
    user = forms.IntegerField(required=False, widget=forms.HiddenInput())
    bookmarked = forms.BooleanField(required=False, widget=forms.HiddenInput())