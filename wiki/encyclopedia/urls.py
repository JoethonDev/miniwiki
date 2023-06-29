from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/newPage", views.createPage, name="newPage"),
    path("wiki/randomPage", views.randomPage, name="randomPage"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.editPage, name="editPage")
]
