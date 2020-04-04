from django.conf.urls import url
from mainapp import views

#template tagging
app_name = 'mainapp'
urlpatterns=[
    url(r'^LogIn/$',views.user_logIn,name='LogInPage'),
    url(r'^SignUp/$',views.signUp,name='SignUpPage'),
    url(r'^welcome/$',views.welcome,name='welcomePage'),
]
