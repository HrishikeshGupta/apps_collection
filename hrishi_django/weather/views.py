import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
import os

API_KEY = os.environ.get('API_KEY_OPENWEATHERMAP')

def validate_city(actual_city,cities):
    if len(cities)==0:
        return(1)
    for each in cities:
        if each.name.lower() == actual_city.lower():
            return(-1)
        else:
            return(1)

def get_unique_cities(cities):
    city_list = []
    if cities.count() > 0:
        for city in cities:
            if city.name not in city_list:
                city_list.append(city.name)
                if len(city_list) ==4:
                    return(city_list)
    return(city_list)

def weather(request):
    bool_new_city = 1
    cities = City.objects.all().order_by('-created_at')
    actual_city = request.POST.get('name')

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()    
    context = {}    
    weather_data = []
    city_weather = {}
    cities = City.objects.all().order_by('-created_at')
    final_top_cities = get_unique_cities(cities)
    for city in final_top_cities:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
        r = requests.get(url.format(city,API_KEY)).json()
        if r.get('message') != "city not found":
            temperature = round((int(r['main']['temp']-32) * 5/9),2)
            city_weather = {
                'city' : city.upper(),
                'country': r['sys']['country'],
                'temperature' : temperature,
                'description' : (r['weather'][0]['description']).upper(),
                'icon' : r['weather'][0]['icon'],
            }
            weather_data.append(city_weather)
            
        else:
            if str(actual_city) == str(city):
                context['missing_data']=1
    if len(weather_data) >0:
        context['data_availabe']=1
    context['weather_data'] = weather_data
    context['form']= form
    return render(request, 'weather/weather.html', context)
