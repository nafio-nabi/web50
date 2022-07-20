# Capstone Project: Schleplist

## Distinctiveness and Complexity
<br>

### What?
The name of my web application is [schleplist](https://schleplist.herokuapp.com/). It allows users to post tedious, and unpleasant tasks (schleps) that they have to do. Listed below is the functionality of the app:

- Users can sign up, sign in, and sign out.

- Users can create and update their profile.

- Users can write a text-based post that describes their schleps.

- Users can edit any of their own schleps.

- Users can see an index of all schleps from all users.

- Users can see a detailed view of a schleps.

- Users can bookmark a schleps, and remove any of their bookmarked schleps.

- User's can get in touch with site owner via tawk.to (CRM).

<br>

### Why?
I got the idea for [schleplist](https://schleplist.herokuapp.com/) after reading [Paul Graham's](http://www.paulgraham.com/bio.html) essay: [Schlep Blindness](http://www.paulgraham.com/schlep.html). The essay states that most people dislike tedious, unpleasant tasks (schleps) and ignore them. However, good ideas often stem from schleps. The reason why I built [schleplist](https://schleplist.herokuapp.com/) is so that people can write and express their schleps for other's to see. In this way we may be able to see good ideas.

<br>

### How?
I have built [schleplist](https://schleplist.herokuapp.com/) using the following technologies:
- Framework: Django, Bootstrap.
- Languages used: Python, JavaScript.
- Database: Postgresql
- Hosting: Heroku for cloud app hosting, and Cloundinary for static file hosting.

I have used three Django models describing the schema for the app. I have also used JavaScript on the front-end using AJAX to edit post. The application is mobile-responsive adjusts the UI according to mobile, tablet, and browser screens.  
<br>

### Where?
See the project here: [schleplist](https://schleplist.herokuapp.com/).

<br>

### Files

#### models.py
````python
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    cloud_profile_image = CloudinaryField('image', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class NewPost(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False)
    body = models.TextField(max_length=640, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Bookmark(models.Model):
    post = models.ForeignKey(NewPost, on_delete=models.CASCADE, related_name='post_bookmark')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookmark')
    created_at = models.DateTimeField(auto_now_add=True)
    bookmarked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post}"
````

#### views.py
````python
import django
from django.shortcuts import render, reverse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from cloudinary.forms import cl_init_js_callbacks

from .forms import SignUpForm, SignInForm, NewPostForm, ImageUploadForm, BookmarkForm
from .models import User, NewPost, Bookmark

# Create your views here.

# index
def index(request):
    return render(request, 'schleplist/index.html')


# signup
def signup(request):
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            first_name = signup_form.cleaned_data['first_name']
            last_name = signup_form.cleaned_data['last_name']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            try:
                user = User.objects.create_user(email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            except IntegrityError:
                return render(request, "schleplist/signup.html", {
                    "message": "This email has already been used",
                    "signup_form": SignUpForm()
                })
            login(request, user)
            return HttpResponseRedirect(reverse("all_posts"))      
    signup_form = SignUpForm()
    return render(request, 'schleplist/signup.html', {
        "signup_form": signup_form
    })


# signout
@login_required(login_url='/signin/')
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# signin
def signin(request):
    if request.method == "POST":
        signin_form = SignInForm(request.POST, request.FILES)
        if signin_form.is_valid():
            email = signin_form.cleaned_data["email"]
            password = signin_form.cleaned_data["password"]
            
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("all_posts"))   
            else:
                return render(request, "schleplist/signin.html", {
                    "message": "Invalid username and/or password",
                    "signin_form": SignInForm()
                }) 
    signin_form = SignInForm()
    return render(request, "schleplist/signin.html", {
        "signin_form": signin_form
    })


# new post
@login_required(login_url='/signin/')
def new_post(request):
    if request.method == "POST":
        new_post_form = NewPostForm(request.POST)
        if new_post_form.is_valid():
            title = new_post_form.cleaned_data["title"]
            body = new_post_form.cleaned_data["body"]
            user = request.user.id
            NewPost.objects.create(title=title, body=body, user_id=user)
            return HttpResponseRedirect(reverse('all_posts'))
    new_post_form = NewPostForm()
    return render(request, "schleplist/new_post.html", {
      "new_post_form": new_post_form  
    })

# edit post
@csrf_exempt
@login_required(login_url='/signin/')
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        new_post = request.POST.get('post')
        new_post_title = request.POST.get('post_title')
        try:
            post = NewPost.objects.get(id=post_id)
            if post.user.id == request.user.id:
                post.title = new_post_title.strip()
                post.body = new_post.strip()
                post.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)
    return JsonResponse({}, status=400)



# all post
def all_post(request):
    all_posts = NewPost.objects.all().order_by("-created_at")
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "schleplist/all_posts.html", {
        "page_obj": page_obj
    })


# post
def post(request, post_id):
    post = NewPost.objects.get(id=post_id)
    bookmark = Bookmark.objects.filter(post_id=post_id, user_id=request.user.id)
    bookmarked = None
    if bookmark:
        bookmark_form = BookmarkForm(initial={"post": post.id, "user": request.user.id, "bookmarked": bookmark.first().bookmarked})
        bookmarked = bookmark.first().bookmarked
    else:
        bookmark_form = BookmarkForm(initial={"post": post.id, "user": request.user.id, "bookmarked": False})
        bookmarked = False
    return render(request, "schleplist/post.html", {
        "post": post,
        "bookmark_form": bookmark_form,
        "bookmarked": bookmarked
    })


# bookmarks
@login_required(login_url='/signin/')
def bookmarks(request):
    if request.method == "POST":
        bookmark_form = BookmarkForm(request.POST)
        if bookmark_form.is_valid():
            post = bookmark_form.cleaned_data["post"]
            user = bookmark_form.cleaned_data["user"]
            bookmarked = bookmark_form.cleaned_data["bookmarked"]
            if bookmarked == False:
                bookmarked = True
                Bookmark.objects.create(post_id=post, user_id=user, bookmarked=bookmarked)
            else:
                Bookmark.objects.filter(post_id=post, user_id=user, bookmarked=bookmarked).delete()
            return HttpResponseRedirect(reverse('bookmarks'))
    bookmarks = Bookmark.objects.filter(user=request.user.id).all().order_by("-created_at")
    paginator = Paginator(bookmarks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "schleplist/bookmarks.html", {
        "page_obj": page_obj
    })


# profile
@login_required(login_url='/signin/')
def profile(request, user):
    all_posts = NewPost.objects.filter(user=request.user.id).order_by("-created_at")
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "schleplist/profile.html", {
        "page_obj": page_obj
    })


# settings
@login_required(login_url='/signin/')
def settings(request):
    if request.method == "POST":
        image_upload_form = ImageUploadForm(request.POST, request.FILES)
        if image_upload_form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            if request.FILES:
                user.profile_image = request.FILES['profile_image']
                user.cloud_profile_image = request.FILES['profile_image']
            user.save()
            return HttpResponseRedirect(reverse("profile", kwargs={'user':request.user.first_name}))
    image_upload_form = ImageUploadForm(initial={"first_name": request.user.first_name, "last_name": request.user.last_name})
    return render(request, "schleplist/settings.html", {
        "image_upload_form": image_upload_form
    })
````

#### urls.py
````python
from django.urls import path

from .views import index, signup, signout, signin, new_post, all_post, profile, settings, post, bookmarks, edit_post

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('signin/', signin, name='signin'),
    path('new_post/', new_post, name='new_post'),
    path('edit_post/', edit_post, name='edit_post'),
    path('all_posts/', all_post, name='all_posts'),
    path('post/<int:post_id>', post, name='post'),
    path('bookmarks/', bookmarks, name='bookmarks'),
    path('profile/<str:user>', profile, name='profile'),
    path('settings/', settings, name='settings'),
]
````

#### forms.py
````python
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
````

#### Procfile
````python
web: python manage.py migrate && gunicorn project5.wsgi
````

#### requirements.txt
````python
asgiref==3.5.2
certifi==2022.6.15
cloudinary==1.29.0
dj-database-url==0.5.0
Django==4.0.6
django-extensions==3.2.0
django-on-heroku==1.1.2
gunicorn==20.1.0
Pillow==9.2.0
psycopg2-binary==2.9.3
python-decouple==3.6
python-dotenv==0.20.0
six==1.16.0
sqlparse==0.4.2
urllib3==1.26.10
whitenoise==6.2.0

````

#### runtime.txt
````python
python-3.10.5
````


### How to Run the App?
<br>

Clone repository:
```bash
git clone https://github.com/nafio-nabi/schleplist.git
cd schleplist
```

Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

Run development server:
```bash
python manage.py runserver