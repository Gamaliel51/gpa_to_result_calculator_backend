from django.db import models


# Create your models here.
class Userdata(models.Model):
    username = models.CharField(max_length=255)
    saved_results = models.CharField(max_length=10000000)

