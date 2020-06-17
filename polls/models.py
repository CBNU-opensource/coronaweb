from django.db import models

# Create your models here.

class krdaily(models.Model):
    kr_date=models.CharField(max_length=200)
    kr_confirmed=models.CharField(max_length=200)
    kr_death=models.CharField(max_length=200)
    kr_released=models.CharField(max_length=200)
    kr_candidate=models.CharField(max_length=200)
    kr_negative=models.CharField(max_length=200)

    def __str__(self):
        return self.kr_date


class Country(models.Model):
    name = models.CharField(max_length=15)
    information = models.TextField()
    safety = models.IntegerField(default=0)
    entrance = models.CharField(max_length=7)

    def __str__(self):
        return self.name