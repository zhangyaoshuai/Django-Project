from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ContactForm, RentalForm, UserForm
from .models import Contact, Rental
import time

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
    if not request.user.is_authenticated():
        rentals = Rental.objects.all()
        rentalList = list(rentals)
        query = request.GET.get("q")
        if query:
            rentals = rentals.filter(
                Q(title__icontains=query) |
                Q(address__icontains=query) | Q(city__icontains=query)
            ).distinct()
            return render(request, 'visitor_index.html', {
                'rentals': rentals,
            })
        else:
            return render(request, 'visitor_index.html', {'rentals': rentals})
    else:
        rentals = Rental.objects.all()
        query = request.GET.get("q")
        rentalList = list(rentals)
        if query:
            rentals = rentals.filter(
                Q(title__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query)
            ).distinct()
            return render(request, 'index.html', {
                'rentals': rentals,
            })
        else:
            return render(request, 'index.html', {'rentals': rentals})


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                rentals = Rental.objects.all()
                return render(request, 'index.html', {'rentals': rentals})
    context = {
        "form": form,
    }
    return render(request, 'register.html', context)

def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                rentals = Rental.objects.all()
                return render(request, 'index.html', {'rentals': rentals})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')

def log_out(request):
    rentals = Rental.objects.all()
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'visitor_index.html', {'rentals': rentals})

def favorite(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    try:
        if rental.is_favorite:
            rental.is_favorite = False
            rental.favorite_count -= 1
        else:
            rental.is_favorite = True
            rental.favorite_count += 1
        if rental.favorite_count < 0:
            rental.favorite_count = 0
        rental.save()
    except (KeyError, Rental.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def create_rental(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        if request.method == 'POST':
            rental = Rental()
            contact = Contact()
            rental.user = request.user
            rental.title = request.POST['title']
            rental.description = request.POST['description']
            rental.address = request.POST['address']
            rental.address = rental.address.split(',')[0]
            rental.coordinate = request.POST['coordinate']
            rental.price = request.POST['price']
            rental.bedroom = request.POST['bedroom']
            rental.bathroom = request.POST['bathroom']
            rental.city = request.POST['city']
            rental.picture =request.FILES['picture']
            file_type = rental.picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {'error_message': 'Image file must be PNG, JPG, or JPEG',}
                return render(request,'create_rental.html',context)
            contact.email = request.POST['email']
            contact.phone_number = request.POST['phone_number']
            contact.gender = request.POST['gender']
            contact.student_type = request.POST['student_type']
            rental.major = request.POST['major']
            rental.save()
            contact.save()
            return render(request, 'rental_detail.html', {'rental': rental})
        return render(request, 'create_rental.html')


def rental_detail(request):
    pass

def update_rental(request):
    pass

def delete_rental(request):
    pass

def update_contact(request):
    pass





