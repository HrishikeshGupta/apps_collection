from blog.models import Blog
from django.shortcuts import render, redirect
from blog.forms import BlogForm
from django.http import HttpResponse
from django.contrib.auth.models import User,auth


def index(request):
    return HttpResponse("Hello, world. You're at the articles index.")# Create your views here.


def add_blog(request):
    context = {}
    blog_form = BlogForm()
    error = ""
    success = ''
    authors_list = []
    if request.user.is_authenticated:
        if request.method=="POST":
            form=BlogForm(request.POST, request.FILES)
            data = request.POST
            if form.is_valid():
                print(form)
                author_name = request.user.username
                title = data.get('title')
                blog_image = form.cleaned_data.get('blog_image')
                email = request.user.email
                description = data.get('description')
                if blog_image:
                    blog = Blog.objects.create(author_name = author_name,title = title,blog_image = blog_image,
                                email=email,description=description)
                else:
                    blog = Blog.objects.create(author_name = author_name,title = title,blog_image = blog_image,
                                email=email,description=description)
                    
                blog.save()
#                 form.save()
                return redirect('/blog/get_blog')
                return render(request,"blog/add_blog.html",{'form':blog_form,"success":1})
            else:
                error='please fill correctly'
                return render(request,"blog/add_blog.html",{'form':blog_form,"error":error})
        else:
            return render(request,"blog/add_blog.html",{'form':blog_form})
    else:
        error="You must be loggedin to add your Blog! Please Register and Login"
        authors_list = get_blogs_data()
        return render(request,"blog/get_blog.html",{'authors_list':authors_list,'error':error})

def get_blogs_data():
    author_dict={}
    authors_list=[]
    blog_data=Blog.objects.all().order_by('-created_at')
    for each in blog_data:
        author_dict={   
                        "id":each.id,
                        "author_name":each.author_name,
                        "image":each.blog_image,
                        "title":each.title,
                        "email":each.email,
                        "description":each.description,
                        "created_at":each.created_at
                    }
        authors_list.append(author_dict)
    return(authors_list)
    
def get_blog(request):
    authors_list = []
    authors_list = get_blogs_data()
    return render(request,"blog/get_blog.html",{'authors_list':authors_list})

def delete_blog(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        blog_record = Blog.objects.filter(id = id)
        blog_record.delete()
    return redirect('/blog/get_blog')
