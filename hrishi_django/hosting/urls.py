from django.urls import path

from . import views

urlpatterns = [
    path('analytics', views.analytics, name='analytics'),
    path('', views.index, name='index'),
]