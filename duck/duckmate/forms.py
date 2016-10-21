from django import forms
from django.contrib.auth.models import User
from .models import Contact, Rental

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['phone_number', 'email', 'gender', 'student_type', 'major']

class RentalForm(forms.ModelForm):

    class Meta:
        model = Rental
        fields = ['title', 'description', 'address', 'city', 'price', 'bedroom',
                  'bathroom','picture']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
