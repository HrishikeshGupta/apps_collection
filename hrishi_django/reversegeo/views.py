from django.shortcuts import render
import requests
from reversegeo.forms import LatLonDataForm
from reversegeo.models import LatLonData
import overpass

def uniq(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)
  return(output)
  
  
def extract_data(dict_for_adminLevel):
    try:
        del dict_for_adminLevel[0]
    except Exception as e:
        pass
    data = uniq([data[1] for data in sorted(dict_for_adminLevel.items(),reverse=True)])
    
    data = ", ".join(data)
    return(data)


def get_data_from_latlon(latitude, longitude):
    api = overpass.API()
    coordinates = "%f,%f" % (float(latitude), float(longitude))
    response = api.get('is_in(' + coordinates + ')', responseformat="json")
    json_data = str(response)
    dict_for_adminLevel = {}
    administritive_level = []
    data = None 
    flag = 0
    for each in response['elements']:
        try:
            name = each['tags']['name:en']
        except Exception as e:
            try:
                name = each['tags']['name']
            except Exception as e:
                pass
        try:
            Name = str(name)
        except UnicodeEncodeError as e:
            pass
        try:
            administritive_level = each['tags']['admin_level']
            administritive_level_check = int(administritive_level)
            if administritive_level_check > 10:
                administritive_level = 0
        except KeyError:
            administritive_level = 0
        dict_for_adminLevel[int(administritive_level)] = Name  
        if len(dict_for_adminLevel)>0:
            data = extract_data(dict_for_adminLevel)
    return(data)

def get_unique_latest_data():
    data = ''
    data_dict = {}
    latlon_data = LatLonData.objects.order_by('-created_at')
    
    for each in latlon_data:
        lat_lon = (each.lat,each.lon)
        data_dict[lat_lon] = each.data
        
        if len(data_dict) == 5:
            return(data_dict)
    return(data_dict)

def save_if_data_exist(lat,lon):
    flag_saved = 0
    lat_lon = LatLonData.objects.filter(lat=lat,lon=lon).first()
    if lat_lon:
        data = lat_lon.data
        data_set = LatLonData(lat=lat,lon=lon,data=data)
        data_set.save()
        flag_saved = 1
    return(flag_saved)
        
        
        
    
def reversegeo(request):
    context = {}
    lat_lon_data = []
    latlondata_form = LatLonDataForm()  
    context['form']= latlondata_form
    if request.method == 'POST':
        data = request.POST
        form = LatLonDataForm(request.POST)
        if form.is_valid():
            lat = data.get('lat')
            lon = data.get('lon')
            bool_save_if_data_exist = save_if_data_exist(lat,lon)
            if bool_save_if_data_exist == 0:
                data = get_data_from_latlon(lat,lon)
                if data:
                    data_set = LatLonData(lat=lat,lon=lon,data=data)
                    data_set.save()
                else:
                    context['missing_data']=1
    
    latlon_data = get_unique_latest_data()
    if len(latlon_data)>0:
        for data in latlon_data:
            city_weather = {
                'lat' : data[0],
                'lon': data[1],
                'data' : latlon_data[data],
            }
            lat_lon_data.append(city_weather)
        context['lat_lon_data'] = lat_lon_data
    context['form']= latlondata_form
    if len(lat_lon_data) >0:
        context['data_availabe']=1     
    return render(request,"reversegeo/reversegeo.html",context)  
    