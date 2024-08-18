from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control



@login_required(login_url='login')
@cache_control(must_revalidate=True,no_store=True)
def home(request):
    return render(request,"index.html")



@cache_control(must_revalidate=True,no_store=True)
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confpassword = request.POST.get('confpassword')

        if password != confpassword:
            messages.error(request,"Password do not match")
            
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('signup')
        
        user = User(username = username)
        user.set_password(password)
        user.save()
        messages.success(request,"User created successfully")
        return redirect('login')

    return render(request,"signup.html")

@cache_control(must_revalidate=True,no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            messages.success(request,"User Login Successfull")
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Invalid credentials")
    return render(request,"login.html")

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request,"Logout Successfull")
    return redirect("login")