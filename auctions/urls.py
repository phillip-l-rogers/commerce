"""The url patterns for the Auctions app."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("create_category", views.create_category, name="create_category"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
]
