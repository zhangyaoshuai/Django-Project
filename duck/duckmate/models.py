from __future__ import unicode_literals
from django.db import migrations, models
from django.contrib.auth.models import Permission, User

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0004_alter_user_username_opts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
    ]


class Contact(models.Model):
    user = models.ForeignKey(User, default=1)
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
    student_type = models.CharField(max_length=50, choices=student_type_choices, default=graduate)
    major = models.CharField(max_length=100, default='Computer Science')
    def __str__(self):
        return self.email



class Rental(models.Model):
    user = models.ForeignKey(User, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    bedroom = models.IntegerField(default=1)
    bathroom = models.IntegerField(default=1)
    coordinate = models.CharField(max_length=500,default=None)
    #pub_date = models.DateTimeField('date published')
    picture = models.FileField(default=None)
    is_favorite = models.BooleanField(default=False)
    favorite_count = models.IntegerField(default=0)
    def __str__(self):
        return self.address




