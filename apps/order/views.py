from django.shortcuts import render, redirect
from .models import *

def index(request):
	return render(request, "order/index.html")

# Customer view (menu)
def menu_customer(request, restaurant_id, table_id):
	print(restaurant_id)
	print(table_id)
	request.session["restaurant_id"] = restaurant_id
	request.session["table_id"] = table_id
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

def to_cart(request):
	order = Order.objects.create(restaurant = Restaurant.objects.get(id=request.POST['restaurantid'][0]), table_id = request.session['table_id'], order_status = "pending")
	order_id = order.id
	request.session["orderid"] = order_id
	for i in request.POST.getlist('itemid'):
		Order_item.objects.create(item=Item.objects.get(id=i), order=Order.objects.get(id=order_id), quantity=request.POST['quant[{}]'.format(i)])
	final_order = Order.objects.get(id=order.id)
	for i in final_order.get_orders.all():
		final_order.order_total += i.item.item_price * i.quantity
	final_order.save()
	print(final_order.order_total)
	print(final_order.__dict__)
	print(final_order.get_orders.values())
	return redirect("/restaurantid="+request.POST["restaurantid"][0]+"/tableid="+request.session["table_id"]+"/checkout")

def checkout(request, restaurant_id, table_id):
	this_order = Order.objects.filter(id=request.session["orderid"])
	this_restaurant = Restaurant.objects.filter(id=restaurant_id)
	print(this_order[0].id)
	this_items = Order_item.objects.filter(order=this_order[0])

	for item in this_items:
		print(item.quantity)

	dict = {
		'this_items' : Order_item.objects.filter(order=this_order[0]),
		'this_restaurant' : this_restaurant[0],
		'this_order' : this_order[0]
	}
	return render(request, "order/checkout.html", dict)

def order_placed(request):
	this_order = Order.objects.get(id=request.session["orderid"], table_id=request.session["table_id"])
	this_order.status="Order placed"
	this_order.save()

	this_restaurant = Restaurant.objects.filter(id=request.session["restaurant_id"])
	print(this_order.id)
	this_items = Order_item.objects.filter(order=this_order)

	dict = {
		'this_items' : Order_item.objects.filter(order=this_order),
		'this_restaurant' : this_restaurant[0],
		'this_order' : this_order
	}
	return render(request, "order/orderstatus.html", dict)

def order_track(request):
	this_order = Order.objects.get(id=request.session["orderid"], table_id=request.session["table_id"])
	this_order.status="Order placed"
	this_order.save()

	this_restaurant = Restaurant.objects.filter(id=request.session["restaurant_id"])
	print(this_order.id)
	this_items = Order_item.objects.filter(order=this_order)

	dict = {
		'this_items' : Order_item.objects.filter(order=this_order),
		'this_restaurant' : this_restaurant[0],
		'this_order' : this_order
	}
	return render(request, "order/track_order.html", dict)
# Create your views here.
