from django.test import TestCase

# Create your tests here.
from recommendapp.models import Venues

ob = Venues.objects.get(venue_id = 101759)
print(len(ob))