from django.shortcuts import render
from .forms import UserForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def index(req):
    return render(req,'mainapp/index.html')

def user_logIn(request):
    if request.method == 'POST':
        # First get the username and password supplied
        # print("hello")
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username,password)
        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('mainapp:welcomePage'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            # return HttpResponse("Invalid login details supplied.")
            messages.error(request,'Incorrect username or password')
            return redirect('mainapp:LogInPage')
    else:
        return render(request,'mainapp/login.html')

@login_required
def welcome(req):
    return render(req,'mainapp/welcome.html')

def signUp(req):

    if req.method == 'POST':
        user_form = UserForm(data=req.POST)
        if user_form.is_valid():
            # username = req.POST.get('usrname')
            # fname = req.POST.get('fname')
            # lname = req.POST.get('lname')
            # email = req.POST.get('email')
            # # phno = req.POST.get('phno')
            # passw = req.POST.get('pass')

            # user_form = UserForm(username=username,first_name=fname,last_name=lname,email=email,password=passw)
            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()

            return HttpResponseRedirect(reverse('mainapp:LogInPage'))
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    return render(req,'mainapp/signup.html')
