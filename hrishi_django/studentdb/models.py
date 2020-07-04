from django.db import models
from datetime import datetime    
  

class Student_data(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    email = models.EmailField(max_length=254,primary_key=True   )
    dob = models.DateField('DOB')
    qualification = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    specialization = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return(self.name)
    class Meta:  
        db_table = "studwent_data"  