from django.shortcuts import render, redirect
from .models import *

def index(request):
	return render(request, "order/index.html")

# Customer view (menu)
def menu_customer(request, restaurant_id, table_id):
	print(restaurant_id)
	print(table_id)
	this_restaurant = Restaurant.objects.filter(id=restaurant_id)
	if this_restaurant:
		items = Item.objects.filter(restaurant=this_restaurant[0])
		for item in items:
			print(item.item_name)
	dict = {
		'items' : Item.objects.filter(restaurant=this_restaurant[0]),
		'restaurant' : this_restaurant[0]
	}
	return render(request, "order/menu.html", dict)


def display_active_orders(request):
	all_order = Order.objects.all()
	context = {
		"orders":all_order,
	}
	return render(request,"order/active_orders.html",context)
# Create your views here.



