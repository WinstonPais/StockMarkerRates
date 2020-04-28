from django.shortcuts import render,get_object_or_404
from .forms import UserForm,UpdateForm
from mainapp.sample import yfinancesymb,test,getmystocks,getstockdetails
from mainapp.models import UserStockDetails

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import UpdateView
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

# @login_required
# class WelcomeView(DeleteView):
#
#     mystocks=getmystocks(user)
#     context_object_name = 'mainapp/welcome.html'
#     context['mystocks']=mystocks
#     model = UserStockDetails
#     success_url = reverse_lazy("mainapp:welcomePage")

# class StockUpdateView(UpdateView):
#     template_name = "mainapp/update_stock.html"
#     fields = ("purchaseDate","quantity")
#     model = UserStockDetails

@login_required
def StockUpdateView(req,**kwargs):
    if req.method == 'POST':
        print("Hello")
        update_form = UpdateForm(data=req.POST)
        if update_form.is_valid():
            a=req.POST.get('purchaseDate')
            b=req.POST.get('quantity')
            obj2=get_object_or_404(UserStockDetails,id=kwargs['pk'])
            print(a,b)
            obj2.purchaseDate=a
            obj2.quantity=b
            obj2.save()
            return HttpResponseRedirect(reverse('mainapp:welcomePage'))

    c={}
    obj=get_object_or_404(UserStockDetails,id=kwargs['pk'])
    c['date']=str(obj.purchaseDate)
    c['q']=obj.quantity
    c['pkk']=kwargs['pk']

    return render(req,'mainapp/update_stock.html',c)

@login_required
def dele(req,**kwargs):
    print(kwargs['pk'])
    obj=get_object_or_404(UserStockDetails,id=kwargs['pk'])
    if req.method == 'POST':
        obj.delete()
    return HttpResponseRedirect(reverse('mainapp:welcomePage'))

@login_required
def addstock(req):
    if req.method == 'POST':
        symbol = req.POST.get('symbol')
        purchasedate = req.POST.get('pdate')
        quantity = req.POST.get('quantity')
        current_user = req.user

        if(test(symbol)):
            website,costprice,currency,shortName = getstockdetails(symbol,purchasedate)
            today = datetime.datetime.today().isoformat()
            if(purchasedate<=today):
                print(current_user,symbol,purchasedate,quantity)
                tx=UserStockDetails(user=current_user,purchaseDate=purchasedate,symbol=symbol,quantity=quantity,website=website,costprice=costprice,currency=currency,shortName=shortName)
                tx.save()
                messages.success(req, str(shortName)+" "+str(symbol)+' Added')
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
