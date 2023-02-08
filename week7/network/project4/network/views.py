import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Post, Comment, Follower


def index(request):
    # Current user as owner
    current_user = request.user
    
    # Retrieve all posts 
    posts = Post.objects.all().order_by("id").reverse()

    #Pagination 
    paginator = Paginator(posts, 3) # Show 10 posts per page.

    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    

    return render(request, "network/index.html",{
        "owner": current_user,
        "posts_of_the_page": posts_of_the_page
    })


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

def profile(request, user_id):
    
    # Current user as owner
    profile_user = User.objects.get(id=user_id)
    
    # Find the number of followers of the owner 
    being_followered = Follower.objects.filter(being_followered=profile_user)
    number_of_followers = being_followered.count()

    #Find the number and the list of following user by the owner
    number_following = 0
    followers = Follower.objects.filter(followers=profile_user)
    number_following = followers.count()
    list_following_of_owner = []
    for follower in followers:
        list_following_of_owner.append(follower.being_followered.username)
    
    # Retrieve all posts 
    posts = Post.objects.filter(owner=profile_user).order_by("id").reverse()

    #Pagination 
    paginator = Paginator(posts, 1) # Show 10 posts per page.

    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/profile.html",{
        "user":profile_user,
        "posts": posts,
        "posts_of_the_page": posts_of_the_page,
        "list_following_of_owner": list_following_of_owner,
        "number_of_followers": number_of_followers,
        "number_of_following": number_following
    })

def unfollow(request):
    if request.method == "POST":

        # Access the owner of the post to unfollow by the current user 
        owner_post_username = request.POST["owner_post_username"] 
        owner_post = User.objects.get(username=owner_post_username)
        
        # Access the current user
        current_user_username = request.POST["current_user"]
        current_user = User.objects.get(username=current_user_username)
        
        # Find the relationhsip follower in database to remove
        follower_relationship = Follower.objects.get(being_followered=owner_post, followers=current_user)
        follower_relationship.delete()

        return HttpResponseRedirect(reverse("profile"))

def follow(request):
    if request.method == "POST":

         # Access the owner of the post to follow by the current user
        owner_post_username = request.POST["owner_post_username"] 
        owner_post = User.objects.get(username=owner_post_username)
        
        # Access the current user
        current_user_username = request.POST["current_user"]
        current_user = User.objects.get(username=current_user_username)
        
        # Create new relationhsip follower in database
        new_follower_relationship = Follower(being_followered=owner_post, followers=current_user)
        new_follower_relationship.save()

        return HttpResponseRedirect(reverse("profile"))


def following(request):
    
    # current user 
    current_user = request.user

    # All the following user by user
    follower_relationships = Follower.objects.filter(followers=current_user)
    list_following_of_owner = []
    for follower in follower_relationships:
        list_following_of_owner.append(follower.being_followered.username)
    
    # Retrieve all posts 
    posts = Post.objects.all().order_by("id").reverse()

    #Pagination 
    paginator = Paginator(posts, 2) # Show 10 posts per page.

    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": posts,
        "posts_of_the_page": posts_of_the_page,
        "list_following_of_owner": list_following_of_owner
    })

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
