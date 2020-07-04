from django.shortcuts import render
from django.http import HttpResponse
import os
from writetome.models import WritersData
from reversegeo.models import LatLonData 
from weather.models import City
from studentdb.models import Student_data

# Create your views here.
def index(request):
    return render(request,'hosting/index2.html')

def get_counts_age_wise(student_data):
    under_24 = 0
    under_18 = 0
    others = 0
    
    for each_student in student_data:
        age = each_student.age
        if age < 18:
            under_18 = under_18 +1
        elif (age <24) and (age >=18):
            under_24 = under_24 + 1
        else:
            others = others+1
            
    return(under_18,under_24, others)

def analytics(request):
    context ={}
    writer_data = WritersData.objects.all()
    total_writers_data = writer_data.count()
    
    latlon_data = LatLonData.objects.all()
    total_latlong_data = latlon_data.count()
    
    city_data = City.objects.all()
    total_city = city_data.count()
    
    student_data = Student_data.objects.all()
    total_student_data = student_data.count()
    under_18,under_24, others = get_counts_age_wise(student_data)
    
    
    context['total_writers_data'] = total_writers_data
    context['total_latlong_data'] = total_latlong_data 
    context['total_city'] = total_city 
    context['total_student_data'] = {
                                    "total_student_data":total_student_data,
                                    "under_18":under_18,
                                    "under_24":under_24,
                                    "others":others
                                    }
    
    print(context)
    
    return render(request,'hosting/analytics.html',context)




