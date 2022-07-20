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