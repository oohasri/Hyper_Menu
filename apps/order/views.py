from django.shortcuts import render, redirect
from .models import *
import bcrypt


# import brcypt
from django.contrib import messages

def index(request):
	if "restaurant_name" not in request.session:
		request.session['restaurant_name'] = ""

	return render(request, "order/index.html")

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
		'items': Item.objects.filter(restaurant=this_restaurant[0]),
		'restaurant': this_restaurant[0]
	}
	return render(request, "order/menu.html", dict)

def to_cart(request):
	order = Order.objects.create(restaurant = Restaurant.objects.get(id=request.POST['restaurantid'][0]), table_id = request.session['table_id'], order_status = "pending")
	order_id = order.id
	request.session["orderid"] = order_id
	print(request.POST.getlist('itemid'))
	for i in request.POST.getlist('itemid'):
		if request.POST['quant['+i+']'] != '':
			Order_item.objects.create(item=Item.objects.get(id=i), order=Order.objects.get(id=order_id), quantity=request.POST['quant['+i+']'][0])
			final_order = Order.objects.get(id=order.id)
			# final_order.order_total += i.item.item_price * i.quantity
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
	print(this_order.order_status)
	this_order.order_status="Order placed"
	this_order.save()
	print(this_order.order_status)
	print("aaaaaaaaaaaa")

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

def display_active_orders(request):
	rest_id = request.session['id']
	this_rest = Restaurant.objects.get(id=rest_id)
	all_order = Order.objects.exclude(order_status= "ready")
	all_order = all_order.exclude(order_status="pending")
	all_order=all_order.filter(restaurant=this_rest)
	for order in all_order:
		print("all",order.get_orders.all())
		if not order.get_orders.all():
			print("yes")
		else:
			print("no")
	context = {
		"this_rest":this_rest,
		"orders":all_order,
	}
	return render(request,"order/active_orders.html",context)

def reload_orders(request):
	all_order = Order.objects.all()
	context = {
		"orders":all_order,
	}
	return render(request,"order/active_orders.html")

# register a restaurant
def register(request):
    if request.method != "POST":
        return redirect("/")
    else:
        errors = Restaurant.objects.validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            hash_password = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt())
            print(hash_password)
            Restaurant.objects.create(restaurant_name=request.POST['restaurant_name'], email=request.POST['email'], phone_number=request.POST['phone_number'], location=request.POST['location'], password=hash_password)
            user = Restaurant.objects.filter(email=request.POST['email'])
            request.session['id'] = user[0].id
        return redirect('/order/dashboard')

# login to portal
def login(request):
	if 'id' not in request.session:
		if request.method != "POST":
			return redirect("/")
		else:
			email = request.POST['email']
			password = request.POST['password']
			user = Restaurant.objects.filter(email=email)
			if len(user) == 0:
				messages.error(request, "User not recognized")
				return redirect("/")
			else:
				if bcrypt.checkpw(password.encode(), user[0].password.encode()):
					request.session['id'] = user[0].id
					return redirect('/order/dashboard')
				else:
					messages.error(request, "Invalid password")
					return redirect('/')
	else:
		return redirect('/order/dashboard')

def update_staus(request):
	if request.method == "POST":
		print("hi")
		status = request.POST['order_status']
		order_id = request.POST['order_id']
		this_order = Order.objects.get(id=order_id)
		this_order.order_status = status
		this_order.save()
		return redirect('/order/dashboard')

def display_edit_form(request,order_id):
	this_order = Order.objects.get(id=order_id)
	context = {
		"order" : this_order
	}
	return render(request,"order/edit_order.html",context)

def logout_method(request):
    request.session.flush()
    return redirect('/')

def remove_item(request,order_id,order_item_id):
	this_order_item_id = Order_item.objects.get(id=order_item_id)
	this_order_item_id.delete()
	return redirect('/edit/'+str(order_id))
	
def view_menu(request):
	rest_id = request.session['id']
	this_rest = Restaurant.objects.get(id=rest_id)
	print(this_rest.restaurant_name)
	all_items = Item.objects.filter(restaurant=this_rest)
	context = {
		"list_of_items": all_items,
	}
	return render(request, "order/editmenu.html", context)

def add_item(request):
	if request.method == 'POST':
		new_price = request.POST['new_price']
	
		new_price = float(new_price)
		Item.objects.create(restaurant=Restaurant.objects.get(id=request.session['id']), item_name=request.POST["new_name"], item_description=request.POST["new_desc"], item_price=new_price, item_img_url="none" )
		return redirect("/view_menu")

def edit_item(request,item_id):
		rest_id = request.session['id']
		this_rest = Restaurant.objects.get(id=rest_id)
		edit_this = Item.objects.get(id=item_id)
		print("heloo",edit_this.id)
		context = {
			"this_rest" :this_rest,
			"item_to_edit" : edit_this,
		}
		return render(request, 'order/editpage.html',context)

def add_item_to_order(request,order_id):
	this_order = Order.objects.get(id=order_id)
	rest_id = request.session['id']
	this_rest = Restaurant.objects.get(id=rest_id)
	all_items = Item.objects.filter(restaurant=this_rest)
	context = {
		"this_order" : this_order,
		"list_of_items": all_items,
	}
	return render(request,'order/add_items_order.html',context)

def edit_update_item(request, item_id):
	if request.method == "POST":
		print("heloooooooooo")
		this_item = Item.objects.get(id=item_id)
		item_name = request.POST['edit_name']
		item_desc = request.POST['edit_desc']
		item_price = request.POST['edit_price']
		item_price = float(item_price)
		this_item.item_name = item_name
		this_item.item_price = item_price
		this_item.item_description = item_desc
		this_item.save()
		return redirect('/view_menu')
		 
def create_new_item_order(request):
	if request.method == "POST":
		item_list = request.POST.getlist('item')
		order_id = request.POST['order_id']
		qty = 2
		this_order = Order.objects.get(id=order_id)
		for item in item_list:
			this_item = Item.objects.get(id=item)
			Order_item.objects.create(order=this_order,item=this_item,quantity=qty)
		#total = 0
		for item in this_order.get_orders.all():
			 this_order.order_total += item.item.item_price * qty
			 this_order.save()
		print(this_order.order_total)
		return redirect('/order/dashboard')

		
def delete(request, item_id):
		Item.objects.get(id=item_id).delete()
		return redirect('/view_menu')


		



