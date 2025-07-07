"""Functions that support the various views for the auctions app."""

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Bid, Category, Comment, Listing, User


class BidForm(forms.ModelForm):
    """Form for adding a new bid on a listing."""

    class Meta:
        model = Bid
        fields = ["price"]
        labels = {"price": "Bid"}

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop("listing")  # Pass in the Listing when initializing
        super().__init__(*args, **kwargs)

    def clean_price(self):
        """Verify the price is the starting price or higher than the highest bid."""
        price = self.cleaned_data["price"]
        highest_bid = self.listing.highest_bid()
        if highest_bid:
            current_price = highest_bid.price
            if price <= current_price:
                raise forms.ValidationError(
                    f"Your bid must be higher than the current price (${current_price})."
                )
        else:
            current_price = self.listing.starting_price
            if price < current_price:
                raise forms.ValidationError(
                    "Your bid must be higher than or equal to the starting price "
                    f"(${current_price})."
                )
        return price


class CategoryForm(forms.ModelForm):
    """Form for adding a new category."""

    class Meta:
        model = Category
        fields = ["name", "image_url"]

    def clean_name(self):
        """Verify the category name isn't a duplicate."""
        name = self.cleaned_data["name"]
        if name in Category.objects.all():
            raise forms.ValidationError(
                f"Category already exists with that name ({name})."
            )
        return name


class CommentForm(forms.ModelForm):
    """Form for adding a new comment."""

    class Meta:
        model = Comment
        fields = ["text"]


class ListingForm(forms.ModelForm):
    """Form for creating a new Listing."""

    class Meta:
        model = Listing
        fields = ["title", "category", "description", "image_url", "starting_price"]


@login_required
def categories(request: HttpRequest) -> HttpResponse:
    """Render the auctions categories page."""
    return render(
        request, "auctions/categories.html", {"categories": Category.objects.all()}
    )


@login_required
def category(request: HttpRequest, category_id: int) -> HttpResponse:
    """Render the auctions category page."""
    category = Category.objects.get(pk=category_id)
    listings = category.listings.filter(active=True).all()
    return render(
        request, "auctions/category.html", {"category": category, "listings": listings}
    )


@login_required
def close_listing(request: HttpRequest, listing_id: int) -> HttpResponse:
    """Close the listing."""
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    return redirect("listing", listing_id=listing.id)


@login_required
def comment(request: HttpRequest, listing_id: int) -> HttpResponse:
    """Save the comment for the `Listing` and return to listing page."""
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = CommentForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
    return redirect("listing", listing_id=listing.id)


@login_required
def create_category(request: HttpRequest) -> HttpResponse:
    """Render the auctions create_category page that supports GET and POST."""
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = CategoryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect("category", category_id=category.id)
    else:
        form = CategoryForm()
    return render(request, "auctions/create_category.html", {"form": form})


@login_required
def create_listing(request: HttpRequest) -> HttpResponse:
    """Render the auctions listing page that supports GET and POST."""
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = ListingForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.active = True
            listing.save()
            return redirect("listing", listing_id=listing.id)
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {"form": form})


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """Render the auctions index page."""
    return render(
        request,
        "auctions/index.html",
        {
            "listings": Listing.objects.filter(active=True).all(),
        },
    )


@login_required
def listing(request: HttpRequest, listing_id: int) -> HttpResponse:
    """Render the auctions listing page that supports GET and POST."""
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        bid_form = BidForm(request.POST, listing=listing)
        # Check if form data is valid (server-side)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.user = request.user
            bid.listing = listing
            bid.save()
            return redirect("listing", listing_id=listing.id)
    else:
        bid_form = BidForm(listing=listing)
    comment_form = CommentForm()
    return render(
        request,
        "auctions/listing.html",
        {"listing": listing, "bid_form": bid_form, "comment_form": comment_form},
    )


def login_view(request: HttpRequest) -> HttpResponse:
    """Render the auctions login view page that supports GET and POST."""
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(
            request,
            "auctions/login.html",
            {"message": "Invalid username and/or password."},
        )
    return render(request, "auctions/login.html")


def logout_view(request: HttpRequest) -> HttpResponse:
    """Render the auctions logout view page."""
    logout(request)
    return redirect("index")


def register(request: HttpRequest) -> HttpResponse:
    """Render the register new user page that supports GET and POST."""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")


@login_required
def toggle_watchlist(request: HttpRequest, listing_id: int) -> HttpResponse:
    """Add or remove listing from user's watchlist."""
    listing = Listing.objects.get(pk=listing_id)
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)
    return redirect("listing", listing_id=listing.id)


@login_required
def watchlist(request: HttpRequest) -> HttpResponse:
    """Render the auctions watchlist page."""
    return render(
        request,
        "auctions/watchlist.html",
        {
            "listings": request.user.watchlist.all(),
        },
    )
