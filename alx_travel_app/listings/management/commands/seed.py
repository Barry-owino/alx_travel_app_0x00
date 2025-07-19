from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review
from django.contrib.auth import get_user_model
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews.'

    def handle(self, *args, **kwargs):
        # Clear old data (optional)
        Listing.objects.all().delete()
        Booking.objects.all().delete()
        Review.objects.all().delete()

        # Create sample users
        users = []
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            users.append(user)

        # Create Listings
        for _ in range(10):
            listing = Listing.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(),
                price=random.randint(1000, 10000),
                location=fake.city(),
                available=True
            )

            # Create random bookings for each listing
            for _ in range(random.randint(1, 3)):
                Booking.objects.create(
                    listing=listing,
                    user=random.choice(users),
                    start_date=fake.date_this_year(),
                    end_date=fake.date_this_year()
                )

            # Optional: create reviews
            for _ in range(random.randint(0, 2)):
                Review.objects.create(
                    listing=listing,
                    user=random.choice(users),
                    rating=random.randint(1, 5),
                    comment=fake.sentence()
                )

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded the database.'))

