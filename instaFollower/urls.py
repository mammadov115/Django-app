from django.urls import path
from . import views

urlpatterns = [  
    path("",views.home,name="home"),
    path("login/", views.log_in, name="login"),
    path("log-out",views.log_out,name='log-out'),
    path("sign-up/",views.sign_up,name="sign-up"),
    path('add/',views.add,name='add')

]
