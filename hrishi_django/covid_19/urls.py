from django.urls import path

from . import views

urlpatterns = [
    path('', views.covid19, name='covid19'),
    path('view_in_graph',views.view_in_graph,name='view_in_graph'),
]