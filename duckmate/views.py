import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView, TemplateView, RedirectView, DeleteView, \
    DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Rental
from .forms import LoginForm, RegisterForm

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']



def send_email(request):
    pass

def activate(request, user_id):
    pass

class IndexTemplateView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Welcome to duckmate'
        return context

class RentalListView(ListView):
    template_name = 'rentals.html'
    model = Rental
    context_object_name = 'rentals'


def rentals(request):
    rentals = Rental.objects.all()
    if request.method == "POST":
        query = request.POST['query']
        if query:
            rentals = rentals.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(address__icontains=query) | Q(city__icontains=query)
            ).distinct()
    jsonResults = []
    if rentals:
        for rental in rentals:
            if rental.coordinate != "":
                features = {
                    "coordinate": [float(rental.coordinate.split(',')[0]), float(rental.coordinate.split(',')[1])],
                    "id": int(rental.id),
                    "slug": rental.slug,
                    "city": rental.city,
                    "address": rental.address,
                    "bedroom": int(rental.bedroom),
                    "bathroom": int(rental.bathroom),
                    "favorite_count": int(rental.total_likes),
                    "picture": rental.picture.url,
                    "price": int(rental.price),
                    "phone_number": int(rental.phone_number),
                    "email": rental.email,
                    "gender": rental.gender,
                    "student_type": rental.student_type,
                    "major": rental.major,
                    "time_created": rental.timestamp.isoformat()
                }
                jsonResults.append(features)
    return render(request, 'rentals.html', {'rentals': rentals, 'response': jsonResults})


#return json response for ajax request
@csrf_exempt
def getRentals(request):
    rentals = Rental.objects.all()
    if request.method == "POST":
        #get query from user
        query = request.POST['query']
        if query:
            rentals = rentals.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(address__icontains=query) | Q(city__icontains=query)
            ).distinct()

    jsonResults = [] #json response to ajax

    if rentals:
        for rental in rentals:
            if rental.coordinate != "":
                features = {
                    "coordinate": [float(rental.coordinate.split(',')[0]), float(rental.coordinate.split(',')[1])],
                    "id": int(rental.id),
                    "slug": rental.slug,
                    "city": rental.city,
                    "address": rental.address,
                    "bedroom": int(rental.bedroom),
                    "bathroom": int(rental.bathroom),
                    "favorite_count": int(rental.total_likes),
                    "picture": rental.picture.url,
                    "price": int(rental.price),
                    "phone_number": int(rental.phone_number),
                    "email": rental.email,
                    "gender": rental.gender,
                    "student_type": rental.student_type,
                    "major": rental.major,
                    "time_created": rental.timestamp
                }
                jsonResults.append(features)

    return JsonResponse(jsonResults, safe=False)

class RegisterFormView(FormView):
    pass

class RegisterFormView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('duckmate:rentals')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect('duckmate:rentals')
        else:
            return super(RegisterFormView, self).dispatch(self,*args, **kwargs)

    def form_valid(self, form):
        form.save()
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


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

class LoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('duckmate: rentals')
    def form_valid(self, form):
        form.save()
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


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

def password_reset(request):
    pass

def account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = user.rental_set.all()
    likes = user.likes.all()
    return render(request, 'account.html', {'posts': posts, 'likes': likes})

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
            success = False
        else:
            # add a new like for a rental
            rental.likes.add(user)
            success = True
        ctx = {'likes_count': rental.total_likes, 'success': success}
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
            phone_number = request.POST['phone_number']
            rental.phone_number = request.POST['phone_number']
            email = request.POST['email']
            rental.email = request.POST['email']
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
                        return HttpResponseRedirect('duckmate:rentals')
                    else:
                        render(request, 'create_rental.html')
                return JsonResponse(error)
            else:
                error = {
                    "error": "you already posted this rental, please post another one!"}
                return render(request, 'create_rental.html', error)
        return render(request, 'create_rental.html')



#rental detail
class RentalDetailView(DetailView):
    template_name = 'rental_detail.html'
    model = Rental

def rental_detail(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    return render(request, 'rental_detail.html', {'rental': rental, 'rental_id': rental_id})


def update_rental(request, rental_id):
    pass

def delete_rental(request, rental_id):
    pass





