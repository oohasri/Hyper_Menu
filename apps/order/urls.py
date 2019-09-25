from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^restaurantid=(?P<restaurant_id>\d+)/tableid=(?P<table_id>\d+)$', views.menu_customer),
	url(r'^register$', views.register),
]