from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createAuction", views.createAuction, name="createAuction"),
    path("auctions/<int:id>", views.auctionPage, name="auctionPage"),
    path("auctions/watchlist", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:categoryStr>", views.categories, name="categories"),
]
