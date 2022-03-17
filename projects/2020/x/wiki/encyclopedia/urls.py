from unicodedata import name
from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/random_page/", views.random_page, name="random_page"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/new_page/", views.new_page, name="new_page"),
    path("wiki/<str:title>/edit_page/", views.edit_page, name="edit_page"),
    path("wiki/<str:title>/submit_edits/", views.submit_edits, name="submit_edits")
]
