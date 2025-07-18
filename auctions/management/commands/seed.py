# auctions/management/commands/seed.py

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from auctions.models import Bid, Category, Comment, Listing

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with test users and auction listings"

    def handle(self, *args, **options):
        # Create users
        users = [
            {"username": "alice", "email": "alice@example.com", "password": "testpass"},
            {"username": "bob", "email": "bob@example.com", "password": "testpass"},
            {
                "username": "charlie",
                "email": "charlie@example.com",
                "password": "testpass",
            },
        ]
        for u in users:
            if not User.objects.filter(username=u["username"]).exists():
                User.objects.create_user(
                    username=u["username"], email=u["email"], password=u["password"]
                )
        alice = User.objects.get(username="alice")
        bob = User.objects.get(username="bob")
        charlie = User.objects.get(username="charlie")
        self.stdout.write(self.style.SUCCESS("✅ Users created"))
        # Create categories
        electronics = Category.objects.get_or_create(name="Electronics")[0]
        fashion = Category.objects.get_or_create(name="Fashion")[0]
        # Create listings
        Listing.objects.get_or_create(
            title="Smartphone",
            description="Brand new smartphone with latest features.",
            starting_bid=300,
            image_url="https://tse3.mm.bing.net/th/id/OIP.tXefyRx69wGNHqj5MoXYDAHaLl",
            category=electronics,
            user=alice,
            active=True,
        )
        Listing.objects.get_or_create(
            title="Leather Jacket",
            description="Stylish leather jacket, gently used.",
            starting_bid=80,
            image_url="https://di2ponv0v5otw.cloudfront.net/posts/2022/12/30/63af446d02760b0ef737b617/m_63af44d902760b00e637b9d4.jpg",
            category=fashion,
            user=bob,
            active=True,
        )
        listing = Listing.objects.get(title="Smartphone")
        Bid.objects.create(amount=350, user=bob, listing=listing)
        Comment.objects.create(user=charlie, listing=listing, content="Is it unlocked?")
        self.stdout.write(self.style.SUCCESS("✅ Listings and categories created"))
