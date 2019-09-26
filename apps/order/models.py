from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')



class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['restaurant_name']) < 2:
            errors['restaurant_name'] = "First name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Not a valid email"
        elif len(self.filter(email = postData['email'])) > 0:
            errors['email'] = "User already exist"
        if len(postData['location']) < 4:
            errors['location'] = "Location name should be at least 4 characters"
        if len(postData['password']) < 4:
            errors['password'] = "Password should be at least 4 characters"
        if postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = "Passwords do not match"
        return errors

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="items")
    item_name = models.CharField(max_length=100)
    item_price = models.FloatField()
    item_description = models.TextField()
    item_img_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="orders")
    table_id = models.IntegerField()
    order_status = models.CharField(max_length=10, default="pending")
    order_total = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order_item(models.Model):
    item = models.ForeignKey(Item, related_name="ordered_items")
    order = models.ForeignKey(Order, related_name="get_orders")
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# Create your models here.
