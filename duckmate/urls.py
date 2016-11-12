from django.conf.urls import url
from . import views

app_name = 'duckmate'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^log_out/$', views.log_out, name='log_out'),
    url(r'^(?P<rental_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^log_in/create_rental/$', views.create_rental, name='create_rental'),
    url(r'^(?P<rental_id>[0-9]+)/$', views.rental_detail, name='rental_detail')

]