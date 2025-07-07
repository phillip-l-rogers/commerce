"""Classes for the various models in the database for the auctions app."""

from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model for a user which username, email, and password fields."""

    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchers")


class Category(models.Model):
    """Model for a category which includes the name, picture, and created fields."""

    name = models.CharField(max_length=64)
    image_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.name)

    def active_count(self) -> int:
        """Get the active count of the listings."""
        return self.listings.filter(active=True).count()


class Listing(models.Model):
    """Model for a listing which includes the user, name, picture, and created fields."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="listings",
    )
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True)
    starting_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=Decimal("0.01")
    )
    image_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.title)

    def highest_bid(self) -> "Bid | None":
        """Return the `Bid` with the highest price."""
        return self.bids.order_by("-price").first()

    def num_bids(self) -> int:
        """Return the number of bids for the `Listing`."""
        return len(self.bids.all())

    def price(self) -> Decimal:
        """The current price, which is either the starting price or the highest bid."""
        bid = self.highest_bid()
        return bid.price if bid else self.starting_price


class Bid(models.Model):
    """Model for a listing which includes the user, listing, price, and placed fields."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    placed = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.price} on {self.listing}"


class Comment(models.Model):
    """Model for a comment which includes the user, listing, text, and created fields."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.text} on {self.listing}"
