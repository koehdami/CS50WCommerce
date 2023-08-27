from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auctions, Watchlist, Bids, Comments


auctionCategories = ["Electronics", "Fashion", "Home", "Collectibles", "Sports"]



def index(request):
    return render(request, "auctions/index.html", {
        "Auctions":Auctions.objects.all()
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


@login_required(redirect_field_name="",login_url="/login")
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


@login_required(redirect_field_name="",login_url="/login")
def createAuction(request):
    if request.method == "POST":
        picture = request.POST["picture"]
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["categories"]
        if category == "":
            return HttpResponse("category failed")
        new_auction = Auctions(owner_id=request.user, picture=picture, title=title, description=description, price=price, category=category, open=True)
        new_auction.save()
        return render(request, "auctions/createAuction.html", {
            "message":"Auction Created!"
        })
    return render(request, "auctions/createAuction.html", {
        "categories": auctionCategories
    })


def auctionPage(request, id):
                
    # Check if allready on watchlist, create Btn text
    alert = ""
    message = "Add to Watchlist"
    for object in Watchlist.objects.all():
        if object.auctions_id.id == id and object.user_id == request.user:
            message = "Remove from Watchlist"

    # Check if bid exsists, if so check if input bid is higher then existing bid then update else rerender with message
    if request.method == "POST":
        auction = Auctions.objects.get(id = id)
        if "bid" in request.POST:
            if auction.price > int(request.POST["bid"]):
                alert = "Your bid must be higher then the current bid."
                return render(request, "auctions/auctionPage.html", {
                    "auctionData":auction,
                    "message":message,
                    "alert":alert,
                    "comments":Comments.objects.filter(auctions_id=id)
                })
            if Bids.objects.filter(auctions_id=id):
                bidData = Bids.objects.get(auctions_id=id)
                if bidData.bid < int(request.POST["bid"]):
                    bidData.bid = request.POST["bid"]
                    bidData.user_id = request.user
                    auction.price = request.POST["bid"]
                    bidData.save()
                    auction.save()
                else:
                    alert = "Your bid must be higher then the current bid."
                    return render(request, "auctions/auctionPage.html", {
                        "auctionData":auction,
                        "message":message,
                        "alert":alert,
                        "comments":Comments.objects.filter(auctions_id=id)
                    }) 
            else:
                auction.price = request.POST["bid"]
                auction.save()
                bidEntrie = Bids(auctions_id=auction, user_id=request.user, bid=request.POST["bid"])
                bidEntrie.save()


        if "auctions_id" in request.POST:
            if Watchlist.objects.filter(auctions_id = id, user_id = request.user):
                message = "Add to Watchlist"
                Watchlist.objects.get(auctions_id = id, user_id = request.user).delete()
            else:
                message = "Remove from Watchlist"
                auctions_id = Auctions.objects.get(id = id)
                watch = Watchlist(user_id=request.user, auctions_id=auctions_id)
                watch.save()
            
        elif "comment" in request.POST:
            if request.POST["comment"]:
                comment = Comments(auctions_id=auction, user_id=request.user, comment=request.POST["comment"])
                comment.save()
            else:
                alert = "Comment must contain letters"
        elif "end_auction" in request.POST:
            try:
                bids = Bids.objects.get(auctions_id=id)
                auction.winner = bids.user_id
            except:
                auction.winner = None
            auction.open = False
            auction.save()
    try: 
        bidsValue = Bids.objects.get(auctions_id=id)
    except:
        bidsValue = 0

    return render(request, "auctions/auctionPage.html", {
        "auctionData":Auctions.objects.get(id=id),
        "message":message,
        "bids":bidsValue,
        "comments":Comments.objects.filter(auctions_id=id),
        "alert":alert
    })

@login_required(redirect_field_name="",login_url="/login")
def watchlist(request):
    auctions = Watchlist.objects.filter(user_id = request.user)
    return render(request, "auctions/watchlist.html", {
        "list":auctions
    })


def categories(request, categoryStr=None):
    print(categoryStr)
    if categoryStr:
        auctions = Auctions.objects.filter(category = categoryStr)
    else:
        auctions = ""
    return render(request, "auctions/categories.html", {
        "categories": auctionCategories,
        "auctions":auctions,
        "categoryStr":categoryStr
    })
