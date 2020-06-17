from django.db import models

class kr_region(models.Model):
    kr_date=models.CharField(max_length=200)
    kr_region=models.CharField(max_length=200)
    kr_confirmed=models.CharField(max_length=200)
    kr_death=models.CharField(max_length=200)
    kr_released=models.CharField(max_length=200)


# Create your models here.
