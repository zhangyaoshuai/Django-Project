from django.test import TestCase
from django.contrib.auth.models import User
from .models import Rental, UserProfile, LikedList


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='eric', email='yzhan65@stevens.edu', password='zys890312')
        User.objects.create(username='zhang', email='zhang890312@gmail.com', password='zys900417')

class RentalTestCase(TestCase):
    def setUp(self):
        pass

class LikedListTestCase(TestCase):
    def setUp(self):
        pass

