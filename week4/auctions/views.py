from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category,Listing, Comment, Bid, Watch_list


def index(request):
    #get all the listing items in database
    listings = Listing.objects.all()

    return render(request, "auctions/index.html",{
        "listings": listings
    })

def Listing_information(request, listing_id):

    #Get only one listing item in database which meets condition: listing_id
    listing_item = Listing.objects.get(pk=listing_id)

    #take the current user logged in
    current_user = request.user

    #active status 
    isActive = listing_item.active

    # Get all the comments in database which meet condition: listing_item
    comments = Comment.objects.filter(listing_comment=listing_item)

    # Detect the winner 
    winner = listing_item.winner

    #Get all the bids in databse which meet conditions: listing_item
    bids = Bid.objects.filter(listing_bid = listing_item)
    number_of_bids = len(bids)
    return render(request, "auctions/listing_information.html", {
        "listing_item": listing_item,
        "current_user": current_user,
        "comments": comments,
        "bids": bids,
        "number_of_bids": number_of_bids,
        "active_status": isActive,
        "winner": winner
    })

def bid(request):
    if request.method == "POST":

        #Get the current bid from user via form 
        bid_detail = float(request.POST["bid"])

        #take the current user logged in
        current_user = request.user
        listing_id = request.POST["listing_item_id"]
        listing_item = Listing.objects.get(pk=listing_id)

        #Take all the objects in Bid class, which meet conditionL listing_item
        previous_bids_objects = Bid.objects.filter(listing_bid=listing_item)

        #create all the bids in number form, collecting the attributes: bid in class Bid
        previous_bids_detail = []
        for bids_object in previous_bids_objects:
            previous_bids_detail.append(bids_object.bid) 

        # Take the initial price from the listing item defined above 
        initial_price = listing_item.initial_price

        # Find the highest value of bid in both initial price and previous bids
        previous_bids_detail.append(initial_price)
        current_max_bid = max(previous_bids_detail)

        # Check the condition of current bid 
        if (bid_detail <= current_max_bid):
            return render(request, "auctions/error.html",{
                "listing_item_id":listing_id
            })
        else:
            new_bid = Bid(
                bid = bid_detail,
                listing_bid = listing_item,
                user_bid = current_user
            )

            new_bid.save()

            return redirect("Listing_information", listing_id= listing_id) 

def closeBid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_item_id"]
        listing_item = Listing.objects.get(pk=listing_id)

        #Change the status of listing item from active into passive 
        listing_item.active = False

        #Take all the objects in Bid class, which meet conditionL listing_item
        previous_bids_objects = Bid.objects.filter(listing_bid=listing_item)

        #create all the bids in number form, collecting the attributes: bid in class Bid
        previous_bids_detail = []
        for bids_object in previous_bids_objects:
            previous_bids_detail.append(bids_object.bid)

        #The highest bid in all bids, find the winner 
        highest_bid_value = max(previous_bids_detail)
        highest_bid = Bid.objects.get(bid = highest_bid_value)
        winner_user = highest_bid.user_bid
        listing_item.winner = winner_user
        listing_item.save()

        return redirect("Listing_information", listing_id= listing_id)
       

def comment(request):

    #add comment from the form 
    if request.method == "POST":
        comment_detail = request.POST["comment"]
        current_user = request.user
        listing_id = request.POST["listing_item_id"]
        listing_item = Listing.objects.get(pk=listing_id)

        # create new object in class Comment with all the distributors
        new_comment = Comment(
            comment = comment_detail,
            listing_comment = listing_item,
            user_comment = current_user
        )

        # Save the new object to database
        new_comment.save()

        return redirect("Listing_information", listing_id= listing_id)     

def create_list(request):

    #method is POST (form is sent)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image_URL = request.POST["image"]
        initial_price = request.POST["initial_price"]
        
        # category related to another table(model) category, category name needs to be identfied clear
        category_name = request.POST["category"]
        category = Category.objects.get(group=category_name)

        #check the current user after logging in 
        current_user = request.user

        #create new listing from all the infromation above taken from HTML form
        new_listing = Listing(
            title=title, 
            description=description, 
            image= image_URL, 
            initial_price = float(initial_price),
            category = category,
            owner = current_user
            )
        new_listing.save()

        #redirect to index page
        return HttpResponseRedirect(reverse(index))

    #method is GET (form is shown)  
    else:
        #Take all the categories from the table(model) Category
        categories = Category.objects.all()

        return render(request,"auctions/create_list.html", {
            "categories": categories
        }) 

def category(request, category_id):
    #Get the category is chosen
    category = Category.objects.get(pk= category_id)

    #Find all the listing item belong to thi category
    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/category.html", {
        "category": category,
        "listing_items": listings
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def watch_list(request):
    #method is POST (form is sent)
    if request.method == "POST":
        listing_id = request.POST["listing_item_id"]
        listing_item = Listing.objects.get(pk=listing_id)

        #current user
        current_user = request.user

        #Check available listing items in watch list of current user
        all_listing_item = Watch_list.objects.filter(user_watch_list= current_user)
        
        #check if the listing item in watch list of current user or not
        result = next((
            obj for obj in all_listing_item if obj.list_watch == listing_item),
            None
        )

        #if already have, return error
        if result != None:
            return render(request, "auctions/error_watch_list.html", {
                "listing_item_id": listing_id
            })

        #else not have, then add, then redirect to the wtach list
        else:
            #create and save new listing item in watch list
            new_watch_list = Watch_list(
                user_watch_list = current_user,
                list_watch = listing_item
            )

            new_watch_list.save()

            #Find all the listing items in the current user's watch list
            all_listing_items = Watch_list.objects.filter(user_watch_list=current_user)

            return render(request,"auctions/watch_list.html",{
            "all_listing_items": all_listing_item
            }) 
    else:
        #current user
        current_user = request.user

        #Check available listing items in watch list of current user
        all_listing_item = Watch_list.objects.filter(user_watch_list= current_user)
        
        return render(request,"auctions/watch_list.html",{
            "all_listing_items": all_listing_item
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
