from django import forms 
from studentdb.models import Student_data 


class DateInput(forms.DateInput):
    input_type = 'date' 


class StudentForm(forms.ModelForm):  
    class Meta:  
        model = Student_data  
        fields = "__all__"
        widgets = {
            'dob': DateInput(),
            }

class EmailForm(forms.ModelForm):
    class Meta:  
        model = Student_data  
        fields = ["email"]
        labels = {
            'email': 'Search by email'
        }