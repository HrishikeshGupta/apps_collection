from django.urls import path

from . import views

urlpatterns = [
    path('', views.writer_data_form, name='writer_data_form'),
]