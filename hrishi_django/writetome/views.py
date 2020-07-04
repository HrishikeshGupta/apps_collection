from django.shortcuts import render

# Create your views here.
from writetome.form import WritersDataForm
from django.core.mail import send_mail
import os

def create_message_and_send_email(name,email,country,message):
    try:
        subject = 'User Posted at your site'
        body = "name: {}\nemail: {}\ncountry: {}\nmessage: {}".format(name,email,country,message)
        from_sender  = os.environ.get('USER')
        to_reciever =['hrishi123gupta@gmail.com','vishalnarayan29@gmail.com']
        fail_silently = False
        send_mail(subject,body,from_sender,to_reciever)
    except Exception as e:
        pass

def writer_data_form(request):  
    writers_form = WritersDataForm()  
    if request.method == 'POST':
        data = request.POST
        form = WritersDataForm(request.POST)
        if form.is_valid():
            form.save()
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
            country = data.get('country')
            create_message_and_send_email(name,email,country,message)
        return render(request,"writetome/writer_data.html",{'form':writers_form})  
    else:
        return render(request,"writetome/writer_data.html",{'form':writers_form })  