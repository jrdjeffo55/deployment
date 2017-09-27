# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

# Create your models here.
class Manager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors['first_name'] = "first name must be letters only"
        if not LETTER_REGEX.match(postData['first_name']):
            errors['first_name_valid'] = "first name must be letters only"
        if len(postData["last_name"])<2:
            errors['last_name'] = "last anme must be more than 2 charecters"
        if not LETTER_REGEX.match(postData["last_name"]):
            errors["last_name_valid"] = "Last name must be letters only"
        if len(postData['email'])<1:
            errors['email_valid']="email field cannot be blank"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_valid'] = "email entered is not valid"
        elif User.objects.filter(email=postData['email']):
            errors['email_valid'] = "email is already registered"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters!"
        if postData["password"]!=postData["confirm_password"]:
            errors["confirm_password"] = "Password does not match confirmation"
        return errors
    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(email=postData["email"]):
            errors["login"] = "Email is not registered"
        elif not bcrypt.checkpw(postData["password"].encode() , User.objects.get(email=postData['email']).hash_pw.encode()):
            errors["login"] = "Incorrect password"
        return errors    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hash_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Manager()
        
        