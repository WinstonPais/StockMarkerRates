from django.shortcuts import render
from .forms import UserForm
from mainapp.sample import yfinancesymb,test,getmystocks
from mainapp.models import UserStockDetails

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
import datetime

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
    mystocks=getmystocks(req.user)
    return render(req,'mainapp/welcome.html',{'mystocks':mystocks})

@login_required
def addstock(req):
    if req.method == 'POST':
        symbol = req.POST.get('symbol')
        purchasedate = req.POST.get('pdate')
        quantity = req.POST.get('quantity')
        current_user = req.user
        if(test(symbol)):
            today = datetime.datetime.today().isoformat()
            if(purchasedate<=today):
                print(current_user,symbol,purchasedate,quantity)
                tx=UserStockDetails(user=current_user,purchaseDate=purchasedate,symbol=symbol,quantity=quantity)
                tx.save()
            else:
                messages.error(req,'Invalid Date')

        else:
            messages.error(req,'Invalid Ticker Symbol')

    return render(req,'mainapp/addstock.html')

@login_required
def result(req):
    if req.method == 'POST':
        script, div = yfinancesymb(req.POST['symbol'])
    # myDict={'script':str(resultString)}
    return render(req, 'mainapp/result.html',
            {'script' : script , 'div' : div} )
    # return render(req,'mainapp/result.html')

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def signUp(req):

    if req.method == 'POST':
        user_form = UserForm(data=req.POST)
        if user_form.is_valid():
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
