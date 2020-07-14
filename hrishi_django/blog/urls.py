from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_blog', views.add_blog, name='add_blog'),
    path('get_blog', views.get_blog, name='get_blog'),
    path('delete_blog', views.delete_blog, name='delete_blog'),
    
]
