from django.conf.urls import url
from . import views
from .views import IndexTemplateView, RentalDetailView, RentalListView, LoginFormView,\
    RegisterFormView

app_name = 'duckmate'

urlpatterns = [
    #send email
    url(r'^send_email/$', views.send_email, name='send_email'),

    #index page
    url(r'^$', IndexTemplateView.as_view(), name='index'),

    #all rentals page
    url(r'rentals/$', views.rentals, name='rentals'),

    #ajax request
    url(r'getRentals/$', views.getRentals, name='getRentals'),

    #user register
    url(r'^register/$', views.register, name='register'),

    #user login
    url(r'^log_in/$', views.log_in, name='log_in'),

    #user logout
    url(r'^log_out/$', views.log_out, name='log_out'),

    #user account
    url(r'(?P<user_id>[0-9]+)/account/$', views.account, name='account'),

    #click to like a rental
    url(r'like/$', views.like, name='like'),

    #create a rental
    url(r'(?P<user_id>[0-9]+)/create_rental/$', views.create_rental, name='create_rental'),

    #rental detail page
    url(r'(?P<pk>[0-9]+)/rental_detail/$', views.rental_detail, name='rental_detail'),

    #update a rental post
    url(r'(?P<user_id>[0-9]+)/(?P<rental_id>[0-9]+)/update_rental/$', views.update_rental, name='update_rental'),

    #delete a rental post
    url(r'(?P<user_id>[0-9]+)/(?P<rental_id>[0-9]+)/delete_rental/$', views.delete_rental, name='delete_rental')

]