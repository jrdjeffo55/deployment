# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import * 
import bcrypt
# Create your views here.
def index(request):
    return render(request, "login_registration/index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if errors:
        for error in errors.itervalues():
            messages.error(request, error, extra_tags="reg")
        return redirect('/')
    else:
        user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], hash_pw=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()))
        request.session['id'] = user.id
        request.session['status'] = "registered"
        return redirect("/success")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for error in errors.itervalues():
            messages.error(request, error, extra_tags="log")
        return redirect("/")
    else:
        request.session["id"] = User.objects.get(email=request.POST["email"]).id
        request.session["status"] = "logged in"
        return redirect("/success")

def success(request):
    context = {
        "user" : User.objects.get(id=request.session["id"]).first_name
    }
    return render(request, "login_registration/success.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")