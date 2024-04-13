from django.urls import path
from loginapp import views

urlpatterns = [
    path('',views.index, name="index"),
    path('loginpage',views.loginPage, name="loginPage"),
    path('login',views.login, name="login"),
    path('login/reset', views.reset, name="reset"),
    path('login/register', views.register, name="register"),
    path('login/logout', views.logout, name="logout"),
    path('user/profile', views.goProfile, name="profile"),
    path('user/update', views.update, name="update"),
]