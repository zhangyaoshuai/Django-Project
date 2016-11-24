from __future__ import unicode_literals
from django.db import migrations, models
from django.contrib.auth.models import Permission, User
from django.db.models.signals import post_save
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __str__(self):
          return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

class LikedList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    liked = models.BigIntegerField(default=0)
    def __str__(self):
        return self.liked

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    price = models.IntegerField()
    bedroom = models.IntegerField(default=0)
    bathroom = models.IntegerField(default=0)
    coordinate = models.CharField(max_length=500)
    picture = models.FileField(default=None)
    favorite_count = models.IntegerField(default=0)
    male = 'm'
    female = 'f'
    graduate = 'gra'
    undergraduate = 'under'
    employed = 'employed'
    student_type_choices = (
        (graduate, 'graduate'),
        (undergraduate, 'undergraduate'),
        (employed, 'employed')
    )
    gender_choices = (
        (male, 'male'),
        (female, 'female'),
    )
    phone_number = models.BigIntegerField(default=0)
    email = models.EmailField(max_length=250)
    gender = models.CharField(max_length=10, choices=gender_choices)
    student_type = models.CharField(max_length=50, choices=student_type_choices)
    major = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now, auto_now=False, blank=True)
    updated = models.DateTimeField(default=timezone.now)
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return self.address


