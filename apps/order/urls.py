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
<<<<<<< HEAD
	url(r'^api/order/dashboard$', views.reload_orders),
=======
	url(r'^login$', views.login),
	url(r'^update/status$', views.update_staus),
	url(r'^edit/(?P<order_id>\d+)$', views.display_edit_form),
	url(r'^logout$',views.logout_method),
	url(r'^remove/(?P<order_id>\d+)/(?P<order_item_id>\d+)$',views.remove_item)
>>>>>>> bd282887d848caaa06ae6c49d0d55e6cc71df60d
]