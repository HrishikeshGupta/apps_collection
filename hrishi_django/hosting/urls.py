from django.urls import path

from . import views

urlpatterns = [
    path('analytics', views.analytics, name='analytics'),
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'), 
    path('logout', views.logout, name='logout'),
    path('test_blog', views.test_blog, name='test_blog'),
]