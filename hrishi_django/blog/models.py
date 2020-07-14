from django.db import models

from datetime import datetime

class Blog(models.Model):
    author_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    blog_image = models.ImageField(upload_to = 'static/blog/images/', max_length=255, default = 'static/blog/images/no_image.jpeg' )
    email = models.EmailField(max_length=254)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return(self.title)




