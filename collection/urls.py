from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("artwork/<int:artwork_id>", views.artwork, name="artwork"),
    path("search/artworks/", views.search_artworks, name="search_artworks"),
    path("accounts/profile/", views.index, name="index"),
    path("accounts/register/", views.register, name="register")
]