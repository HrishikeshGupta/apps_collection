from django import forms  
from reversegeo.models import LatLonData  
  
class LatLonDataForm(forms.ModelForm):  
    class Meta:  
        model = LatLonData  
        fields = ['lat','lon'] 
        labels = {
            'lat': 'Latitude',
            'lon': 'Longitude'
        }