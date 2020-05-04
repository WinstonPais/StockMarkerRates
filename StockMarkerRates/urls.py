from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from mainapp import views,urls

urlpatterns = [
    url(r'^$',views.index,name="index"),
    path('admin/', admin.site.urls),
    url(r'^mainapp/',include('mainapp.urls')),
    path('logout/', views.user_logout, name='logout'),
]
