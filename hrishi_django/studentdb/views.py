from .models import Student_data
from studentdb.forms import StudentForm ,EmailForm
from django.shortcuts import  render
 
def studentdb_view_data(request):
    data = {}
    context = {}
    email_form = EmailForm()
    context['form'] = email_form
    data = request.GET
    email = data.get('email')
    if email:
        try:
            user_data = Student_data.objects.filter(email=email).first()
            data = {
                "name":user_data.name,
                "age":user_data.age,
                "dob":user_data.dob,
                "qualification":user_data.qualification,
                "college":user_data.college,
                "address":user_data.address,
                "specialization":user_data.specialization
                }
            context['data']=data
            return render(request,"studentdb/student_view_data.html",context)
        except Exception as e:
            context['error']='Email id doesnot exists'
            return render(request,"studentdb/student_view_data.html",context) 
    return render(request,"studentdb/student_view_data.html",context) 


def studentdb_add_data(request):  
    student_form = StudentForm()  
    error = ""
    success = ''
    
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"studentdb/studentdb_add_data.html",{'form':student_form,"success":1}) 
        else:
            error=1
            return render(request,"studentdb/studentdb_add_data.html",{'form':student_form,'error':error}) 
    else:
        return render(request,"studentdb/studentdb_add_data.html",{'form':student_form}) 