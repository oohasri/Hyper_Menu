from django.shortcuts import render, redirect
from .models import *
# import brcypt
from django.contrib import messages
def index(request):
	if "restaurant_name" not in request.session:
		request.session['restaurant_name'] = ""

	return render(request, "order/index.html")

def register(request):
	if request.method == "POST":
		Restaurant.objects.create(restaurant_name=request.POST["restaurant_name"], email=request.POST["email"], location=request.POST["location"], phone_number=request.POST["phone_number"], password=request.POST['password'])
		request.session['restaurant_name'] = request.POST["restaurant_name"]
		return redirect("/view_menu")

def login(request):
	if request.method == "POST":
		request.session['email'] = request.POST['email']
		restaurant = Restaurant.objects.get(email=request.POST['email'])
		request.session['restaurant_name'] = restaurant.restaurant_name
		# if bcrypt.checkpw(request.POST['password'].encode(), restaurant.password.encode()):
		request.session['id'] = restaurant.id
		messages.success(request, "Sucessfully registered (or logged in)!")
		return redirect('/view_menu')
		# else:
		# 	messages.error(request, "Email or Password is incorrect") 
		# 	return redirect('/')


def view_menu(request):
	context = {
		"list_of_items": Item.objects.all(),
	}
	return render(request, "order/editmenu.html", context)

def add_item(request):
	if request.method == 'POST':
		new_price = request.POST['new_price']
	
		new_price = float(new_price)
		Item.objects.create(restaurant=Restaurant.objects.get(id=request.session['id']), item_name=request.POST["new_name"], item_description=request.POST["new_desc"], item_price=new_price, item_img_url="none" )
		return redirect("/view_menu")

def edit_item(request, item_id):
	if request.method == 'POST':
		edit_this = Item.objects.get(id=item_id)
		edit_this.item_name = request.POST["edit_name"]
		edit_this.item_description = request.POST["edit_desc"]
		price = request.POST["edit_price"]
		price = float(price)
		edit_this.item_price = price
		edit_this.save() 	
		return redirect('/view_menu')
	if request.method == "GET":
		context = {
			'item_to_edit': Item.objects.get(id=item_id)
		}
		return render(request, 'order/editpage.html', context)
	

def delete(request, item_id):
		Item.objects.get(id=item_id).delete()
		return redirect('/view_menu')
# Create your views here.
