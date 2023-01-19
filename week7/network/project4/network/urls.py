
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posting", views.posting, name="posting"),
    path("all_post", views.all_post, name="all_post"),
    path("profile", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follower/<str:being_followered_username>", views.follower, name="follower")
    
]
