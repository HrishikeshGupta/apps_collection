from django.urls import path

from . import views

urlpatterns = [
    path('', views.studentdb_view_data, name='studentdb_view_data'),
    path('add_data', views.studentdb_add_data, name='studentdb_add_data'),
]