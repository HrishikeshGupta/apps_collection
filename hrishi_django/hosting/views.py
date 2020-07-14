from django.shortcuts import render
from django.http import HttpResponse
import os
from writetome.models import WritersData
from reversegeo.models import LatLonData 
from weather.models import City
from studentdb.models import Student_data

from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.models import User,auth
from django.contrib import messages

from blog.models import Blog



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
    context = {}
    if request.user.is_authenticated:
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
        
        f = open('covid_19/temp_data/all_count_data.txt','r')
        covid_19_searches = int(f.read())
        
        blogs = Blog.objects.all()
        total_blogs = blogs.count()
        
        
        context['total_writers_data'] = total_writers_data
        context['total_latlong_data'] = total_latlong_data 
        context['total_city'] = total_city 
        context['total_student_data'] = {
                                        "total_student_data":total_student_data,
                                        "under_18":under_18,
                                        "under_24":under_24,
                                        "others":others
                                        }
        context['covid_19_searches'] = covid_19_searches
        context['total_blogs'] = total_blogs
        
        return render(request,'hosting/analytics.html',context)
    else:
        context['error']="You must be logged in to view this! Please Register/Login"
        return render(request,'hosting/index2.html',context)

def register(request):
    if request.method=='POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.info(request,'user name already taken')
                return render(request,"hosting/register.html")
            elif User.objects.filter(email = email).exists():
                messages.info(request,'email id alreday taken')
                return render(request,"hosting/register.html")
            else:
                user = User.objects.create_user(username = username,
                                                 password = password1,
                                                 first_name = first_name,
                                                 last_name = last_name,
                                                 email = email  
                                                 )
                user.save()
                return render(request,"hosting/login.html")
        else:
            messages.info(request,'Password did not matched')
            return render(request,"hosting/register.html")
    else:
        return render(request,"hosting/register.html")
    
    
def login(request):    
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
         
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request, user)
            #return render(request,"myapp/home.html")
            return render(request,"hosting/index2.html")
        else:
            messages.info(request,'invalid credentials')
            return render(request,"hosting/login.html")
    else:
         
        return render(request,"hosting/login.html")

def logout(request):
    auth.logout(request)
    return render(request,"hosting/index2.html")
           
def test_blog(request):
    return render(request,"hosting/test_blog.html")


