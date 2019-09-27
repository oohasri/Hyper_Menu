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
	url(r'^api/order/dashboard$', views.reload_orders),
	url(r'^login$', views.login),
	url(r'^update/status$', views.update_staus),
	url(r'^edit/(?P<order_id>\d+)$', views.display_edit_form),
	url(r'^logout$',views.logout_method),
	url(r'^remove/(?P<order_id>\d+)/(?P<order_item_id>\d+)$',views.remove_item),
	url(r'^view_menu$', views.view_menu),	
	url(r'^add_item$', views.add_item),
	url(r'^edit_page/(?P<item_id>\d+)$', views.edit_item),
	url(r'edit_page/(?P<item_id>\d+)/update$', views.edit_update_item),
	url(r'^order/add/item/(?P<order_id>\d+)$',views.add_item_to_order),
	url(r'^delete/(?P<item_id>\d+)$', views.delete),
	url(r'^post/order/add/item$',views.create_new_item_order),
]