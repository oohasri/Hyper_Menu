from django.shortcuts import render, redirect
from .models import *
import bcrypt


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
		'items': Item.objects.filter(restaurant=this_restaurant[0]),
		'restaurant': this_restaurant[0]
	}
	return render(request, "order/menu.html", dict)


def display_active_orders(request):
	all_order = Order.objects.exclude(order_status="ready")
	#all_order = Order.objects.all()
	for order in all_order:
		print("all",order.get_orders.all())
		if not order.get_orders.all():
			print("yes")
		else:
			print("no")
	rest_id = request.session['id']
	this_rest = Restaurant.objects.get(id=rest_id)
	context = {
		"this_rest":this_rest,
		"orders":all_order,
	}
	return render(request,"order/active_orders.html",context)
# Create your views here.

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
	


		



