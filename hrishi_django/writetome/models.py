from django.db import models

class WritersData(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    message = models.TextField(max_length=1000)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return(self.name)