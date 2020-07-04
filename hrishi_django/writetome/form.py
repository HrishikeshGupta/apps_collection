from django import forms  
from writetome.models import WritersData  
  
class WritersDataForm(forms.ModelForm):  
    class Meta:  
        model = WritersData  
        fields = "__all__"  