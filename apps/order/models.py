from django.db import models

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name = "items")
    item_name = models.CharField(max_length=100)
    item_price = models.FloatField()
    item_description = models.TextField()
    item_img_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name = "orders")
    table_id = models.IntegerField()
    order_status = models.CharField(max_length = 10)
    order_total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_item(models.Model):
    item = models.ForeignKey(Item, related_name = "ordered_items")
    order = models.ForeignKey(Order, related_name="get_orders")
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






# Create your models here.
