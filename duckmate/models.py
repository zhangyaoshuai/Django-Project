from __future__ import unicode_literals
import PIL as pl # for future use of editing user profile picture
from django.db import models
from django.contrib.auth.models import Permission, User
from django.template.defaultfilters import slugify
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(max_length=40, default=123)
    key_expires = models.DateTimeField(default=timezone.now)
    def __str__(self):
          return "%s's profile" % self.user

'''
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    phone_number = models.BigIntegerField(default=0)
    email = models.EmailField(max_length=250)
'''

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(default="")
    likes = models.ManyToManyField(User, related_name='likes')
    #contact = models.ManyToManyField(Contact, related_name='contact')
    @property
    def total_likes(self):
        """
        Likes for the rental
        :return: Integer: Likes for the rental
        """
        return self.likes.count()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.address)
        super(Rental, self).save(*args, **kwargs)
    title = models.CharField(max_length=100)
    description = models.TextField()
    phone_number = models.BigIntegerField(default=0)
    email = models.EmailField(max_length=250)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    price = models.IntegerField()
    bedroom = models.IntegerField(default=0)
    bathroom = models.IntegerField(default=0)
    coordinate = models.CharField(max_length=500)
    picture = models.FileField(default=None)
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
    gender = models.CharField(max_length=10, choices=gender_choices)
    student_type = models.CharField(max_length=50, choices=student_type_choices)
    major = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now, auto_now=False, blank=True)
    updated = models.DateTimeField(default=timezone.now)
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return self.address






