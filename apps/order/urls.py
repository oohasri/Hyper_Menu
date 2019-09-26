from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^view_menu$', views.view_menu),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^add_item$', views.add_item),
	#url(r'^edit_page$', views.edit_item),
	url(r'^edit_page/(?P<item_id>\d+)$', views.edit_item),
	url(r'edit_page/(?P<item_id>\d+)/update$', views.edit_item),
	url(r'^delete/(?P<item_id>\d+)$', views.delete),
]