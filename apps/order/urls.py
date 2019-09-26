from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^restaurantid=(?P<restaurant_id>\d+)/tableid=(?P<table_id>\d+)$', views.menu_customer),
	url(r'^order/dashboard$', views.display_active_orders),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^update/status$', views.update_staus),
	url(r'^edit/(?P<order_id>\d+)$', views.display_edit_form),
	url(r'^logout$',views.logout_method),
	url(r'^remove/(?P<order_id>\d+)/(?P<order_item_id>\d+)$',views.remove_item)
]