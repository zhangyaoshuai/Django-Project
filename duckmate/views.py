from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.mail import send_mail
from django.core import serializers
from .models import Rental
from .forms import UserForm



IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
    rentals = Rental.objects.all()
    query = request.GET.get("q")
    if query:
        rentals = rentals.filter(
            Q(title__icontains=query) |
            Q(address__icontains=query) | Q(city__icontains=query)
        ).distinct()
    return render(request, 'index.html', {'rentals': rentals})

def showIndex(request):
    rentals = Rental.objects.all()
    query = request.GET.get("q")
    if query:
        rentals = rentals.filter(
            Q(title__icontains=query) |
            Q(address__icontains=query) | Q(city__icontains=query)
        ).distinct()
    jsonResults = {
        "features": []
    }
    for rental in rentals:
        if rental.coordinate != "":
            features = {
                "coordinate": [float(rental.coordinate.split(',')[0]), float(rental.coordinate.split(',')[1])],
                "id": int(rental.id),
                "city": rental.city.encode(encoding="utf-8"),
                "address": rental.address.encode(encoding="utf-8"),
                "bedroom": int(rental.bedroom),
                "bathroom": int(rental.bathroom),
                "favorite_count": int(rental.favorite_count),
                "picture": rental.picture.url,
                "price": int(rental.price),
                "phone_number": int(rental.phone_number),
                "email": rental.email.encode(encoding="utf-8"),
                "gender": rental.gender.encode(encoding="utf-8"),
                "student_type": rental.student_type.encode(encoding="utf-8"),
                "major": rental.major.encode(encoding="utf-8")
            }
            jsonResults["features"].append(features)
    return JsonResponse(jsonResults)

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
                return redirect('/')
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
                return index(request)
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('/')

@login_required
def like(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    try:
        rental.favorite_count += 1
        rental.save()
    except (KeyError, Rental.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

@login_required
def dislike(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    try:
        rental.favorite_count -= 1
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
            rental.email = request.POST['email']
            rental.phone_number = request.POST['phone_number']
            rental.gender = request.POST['gender']
            rental.student_type = request.POST['student_type']
            rental.major = request.POST['major']
            rentals = Rental.objects.all()
            address = []
            for rent in rentals:
                address.append(rent.address)
            if rental.address not in address:
                rental.save()
            #return render(request, 'rental_detail.html', {'rental': rental})
                return redirect('%d/' % int(rental.id))
            else:
                error = {
                    "error": "This post already exists, please post another one!"}
                return render(request, 'create_rental.html', error)
        return render(request, 'create_rental.html')


def rental_detail(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    return render(request, 'rental_detail.html', {'rental': rental})


def update_rental(request, rental_id):
    pass

def delete_rental(request, rental_id):
    pass





