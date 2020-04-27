from django.conf.urls import url
from django.urls import path
from mainapp import views

#template tagging
app_name = 'mainapp'
urlpatterns=[
    url(r'^LogIn/$',views.user_logIn,name='LogInPage'),
    url(r'^SignUp/$',views.signUp,name='SignUpPage'),
    url(r'^welcome/$',views.welcome,name='welcomePage'),
    url(r'^result/$',views.result,name='resultPage'),
    path('addstock/', views.addstock, name='addstockPage'),
    path('delete/<int:pk>/', views.dele, name='delPage'),
]
