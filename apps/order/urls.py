from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^restaurantid=(?P<restaurant_id>\d+)/tableid=(?P<table_id>\d+)$', views.menu_customer),
	url(r'^add_to_cart$', views.to_cart),
	url(r'^restaurantid=(?P<restaurant_id>\d+)/tableid=(?P<table_id>\d+/checkout)$', views.checkout),
	url(r'^place_order$', views.order_placed),
	url(r'^order/track_order$', views.order_track),
	url(r'^order/dashboard$', views.display_active_orders),
	url(r'^register$', views.register),
]