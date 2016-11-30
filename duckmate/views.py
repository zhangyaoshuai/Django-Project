from duck import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Rental
from .forms import UserForm


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def send_email(request):
    subject = "I am an HTML email"
    to = ['zhangys1989@163.com']
    from_email = settings.EMAIL_HOST_USER

    ctx = {
        'user': 'Eric',

    }

    message = get_template('email/email.html').render(ctx)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return HttpResponse('Email sent!')

def activate(request, user_id):
    pass


def index(request):
    return render(request, 'index.html')

def rentals(request):
    rentals = Rental.objects.all()
    if request.method == "POST":
        query = request.POST['query']
        if query:
            rentals = rentals.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(address__icontains=query) | Q(city__icontains=query)
            ).distinct()
    return render(request, 'rentals.html', {'rentals': rentals})


#return jsaon response for ajax request
@csrf_exempt
def getRentals(request):
    rentals = Rental.objects.all()
    if request.method == "POST":
        query = request.POST['query']
        if query:
            rentals = rentals.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(address__icontains=query) | Q(city__icontains=query)
            ).distinct()
    jsonResults = {
        "features": []
    }
    if rentals:
        for rental in rentals:
            if rental.coordinate != "":
                features = {
                    "coordinate": [float(rental.coordinate.split(',')[0]), float(rental.coordinate.split(',')[1])],
                    "id": int(rental.id),
                    "slug": rental.slug.encode(encoding="utf-8"),
                    "city": rental.city.encode(encoding="utf-8"),
                    "address": rental.address.encode(encoding="utf-8"),
                    "bedroom": int(rental.bedroom),
                    "bathroom": int(rental.bathroom),
                    "favorite_count": int(rental.total_likes),
                    "picture": rental.picture.url,
                    "price": int(rental.price),
                    "phone_number": int(rental.phone_number),
                    "email": rental.email.encode(encoding="utf-8"),
                    "gender": rental.gender.encode(encoding="utf-8"),
                    "student_type": rental.student_type.encode(encoding="utf-8"),
                    "major": rental.major.encode(encoding="utf-8"),
                    "time_created": rental.timestamp
                }
                jsonResults["features"].append(features)
    return JsonResponse(jsonResults)

def register(request):
    if request.method == "POST":
        user = User()
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        username = request.POST['username']
        user.email = request.POST['email']
        email = request.POST['email']
        user.password = request.POST['password']
        password = request.POST['password']
        user.set_password(request.POST['password'])
        if not User.objects.filter(email=email).exists():
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/rentals/')
        else:
            error = {'error': 'email address already exists, please sign up with another one!'}
            return render(request, 'register.html', error)
    return render(request, 'register.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/rentals/')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('/log_in/')

def account(request):
    pass

def profile(request):
    pass

#favorite method
@csrf_exempt
def like(request):
    if not request.user.is_authenticated():
        return redirect('/log_in/')
    if request.method == 'POST':
        user = request.user
        rental_id = request.POST.get('id', None)
        rental = get_object_or_404(Rental, pk=rental_id)

        if rental.likes.filter(id=user.id).exists():
            # user has already liked this rental
            # remove like/user
            rental.likes.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a rental
            rental.likes.add(user)
            message = 'You liked this'

        ctx = {'likes_count': rental.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
        return HttpResponse(json.dumps(ctx), content_type='application/json')

#create rental method
def create_rental(request, user_id):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        user = get_object_or_404(User, pk=user_id)
        if request.method == 'POST':
            rental = Rental()
            rental.title = request.POST['title']
            rental.description = request.POST['description']
            rental.address = request.POST['address']
            rental.address = rental.address.split(',')[0]
            rental.coordinate = request.POST['coordinate']
            coordinate = request.POST['coordinate']
            rental.price = request.POST['price']
            rental.bedroom = request.POST['bedroom']
            rental.bathroom = request.POST['bathroom']
            rental.city = request.POST['city']
            rental.picture =request.FILES['picture']
            rental.email = request.POST['email']
            email = request.POST['email']
            rental.phone_number = request.POST['phone_number']
            phone_number = request.POST['phone_number']
            rental.gender = request.POST['gender']
            rental.student_type = request.POST['student_type']
            rental.major = request.POST['major']
            rental.user = user
            if not Rental.objects.filter(coordinate=coordinate).exists():
                rental.save()
                return redirect('%d/rental_detail' % int(rental.id))
            elif Rental.objects.filter(coordinate=coordinate).exists() and not Rental.objects.filter(phone_number=phone_number, email=email).exists():
                error = {
                    "error": "A same rental has already been posted, would you sill like to continue?"
                }
                if request.method == "GET":
                    confirm = request.POST["confirm"]
                    if confirm == "Yes":
                        rental.save()
                        return redirect('%d/rental_detail' % int(rental.id))
                    else:
                        render(request, 'create_rental.html')
            else:
                error = {
                    "error": "you already posted this rental, please post another one!"}
                return render(request, 'create_rental.html', error)
        return render(request, 'create_rental.html')


#rental detail method
def rental_detail(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    return render(request, 'rental_detail.html', {'rental': rental, 'rental_id': rental_id})


def update_rental(request, rental_id):
    pass

def delete_rental(request, rental_id):
    pass





