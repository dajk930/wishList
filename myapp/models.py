from django.db import models
import re
from datetime import datetime
from time import strptime, localtime
import bcrypt

class UserManager(models.Manager):
    def regValidator(self, form):
        fullname = form['name']
        username = form['username']
        password = form['password']
        confirm_pw = form['confirm_pw']

        errors = {}

        if not fullname:
            errors['fullname'] = "*Name cannot be blank"
        elif len(fullname) < 3:
            errors['fullname'] = "*Name must be at least 3 characters."

        if not username:
            errors['reg_username'] = "*Username cannot be blank."
        elif len(username) < 3:
            errors['reg_username'] = "*Username must be at least 3 characters."
        
        if not password:
            errors['reg_password'] = "*Password cannot be blank."
        elif len(password) < 8:
            errors['reg_password'] = "*Password must be at least 8 characters."

        if not confirm_pw:
            errors['confirm_pw'] = "*Please confirm password."
        elif password != confirm_pw:
            errors['confirm_pw'] = "*Passwords do not match."

        return errors
    

    def loginValidator(self, form):
        username = form['login_user']
        password = form['login_password']

        errors = {}

        if not username:
            errors['login_user'] = "Username can not be blank."
        elif not User.objects.filter(username=username):
            errors['login_user'] = "Username not found."
        else:
            if not password:
                errors['login_password'] = "Please provide required password."
                return errors, False
            else:
                user = User.objects.get(username=username)
                if not bcrypt.checkpw(password.encode(), user.password.encode()):
                    errors['login_password'] = "*Incorrect password; please reenter."
            
                return errors, user

        return errors, False

class wishListManager(models.Manager):
    def wishlistValidator(self, form):
        item_product = form['item_product']

        errors = {}

        if not item_product:
            errors['item_product'] = "*Please enter an Item or Product."

        return errors
    
    # def itemValidator(self, form):


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class wishList(models.Model):
    item_product = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name = 'item_product_added', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name = 'liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = wishListManager()