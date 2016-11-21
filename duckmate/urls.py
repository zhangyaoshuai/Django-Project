from django.conf.urls import url
from . import views

app_name = 'duckmate'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'rentals/$', views.rentals, name='rentals'),
    url(r'getRentals/$', views.getRentals, name='getRentals'),
    url(r'^register/$', views.register, name='register'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^log_out/$', views.log_out, name='log_out'),
    url(r'(?P<rental_id>[0-9]+)/like/$', views.like, name='like'),
    url(r'(?P<rental_id>[0-9]+)/unlike/$', views.unlike, name='unlike'),
    url(r'(?P<user_id>[0-9]+)/create_rental/$', views.create_rental, name='create_rental'),
    url(r'(?P<rental_id>[0-9]+)/rental_detail/$', views.rental_detail, name='rental_detail'),
    url(r'(?P<user_id>[0-9]+)/(?P<rental_id>[0-9]+)/update_rental/$', views.update_rental, name='update_rental'),
    url(r'(?P<user_id>[0-9]+)/(?P<rental_id>[0-9]+)/delete_rental/$', views.delete_rental, name='delete_rental')

]