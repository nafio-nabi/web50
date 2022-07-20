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