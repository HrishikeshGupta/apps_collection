from django.db import models

# Create your models here.
from django.db import models

class LatLonData(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    data = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return (str(self.lat)+','+str(self.lon))