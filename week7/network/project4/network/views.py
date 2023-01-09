import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Comment, Follower


def index(request):
    return render(request, "network/index.html")


def posting(request):
    
    # Check the method is POST 
    if request.method == "POST":

        # Retrieve post's content from the html form 
        post_content = request.POST["post_content"]

        # Owner is the present user
        owner = request.user

        # Create the new object POST (model)
        new_post = Post(
            owner = owner,
            content = post_content
        )

        new_post.save()

        return HttpResponseRedirect(reverse("index"))

def all_post(request):

    # Return all the posts of all users in reverse order in JSON form 
    posts = Post.objects.all().order_by("-timestamp")
    return JsonResponse([post.serialize_post() for post in posts], safe=False)

def profile(request):
    owner = request.user
    followers = Follower.objects.get(being_followered=owner)
    #being_followered = Follower.objects.filter(owner in followers)
    number_of_followers = followers.followers.count()
    return render(request, "network/profile.html",{
        "owner": owner,
        "number_of_followers": number_of_followers
    })

def follower(request):
    owner = request.user
    followers = Follower.objects.get(being_followered=owner)
    return JsonResponse([follower.serialize_follow() for follower in followers], safe=False)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
