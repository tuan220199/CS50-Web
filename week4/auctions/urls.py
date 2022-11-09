from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.create_list, name="create_list"),
    path("categories", views.categories, name="categories"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("comment", views.comment, name="comment"),
    path("bid", views.bid, name="bid"),
    path("closeBid", views.closeBid, name="closeBid"),
    path("category/<int:category_id>", views.category, name="category"),
    path("Listing_information/<int:listing_id>", views.Listing_information, name="Listing_information")
]
