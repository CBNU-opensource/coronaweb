from django.db import models

class krdaily(models.Model):
    kr_date=models.CharField(max_length=20)
    kr_confirmed=models.TextField()
    kr_death=models.CharField(max_length=20)
    kr_released=models.CharField(max_length=20)
    kr_candidate=models.CharField(max_length=20)
    kr_negative=models.CharField(max_length=20)

    def __str__(self):
        return self.kr_date

class Country(models.Model):
    name = models.CharField(max_length=15)
    information = models.TextField()
    safety = models.IntegerField(default=0)
    entrance = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class World_daily(models.Model):
    world_today_date=models.CharField(max_length=20)
    world_total_confirmed=models.CharField(max_length=20)
    world_new_cases=models.CharField(max_length=20)
    world_total_death=models.CharField(max_length=20)
    world_new_death=models.CharField(max_length=20)
    world_deaths_rate=models.CharField(max_length=20)
    world_country=models.CharField(max_length=20)

    def __str__(self):
        return self.world_country

class kr_region(models.Model):
    kr_date=models.CharField(max_length=20)
    kr_region=models.CharField(max_length=20)
    kr_confirmed=models.CharField(max_length=20)
    kr_death=models.CharField(max_length=20)
    kr_released=models.CharField(max_length=20)

    def __str__(self):
        return self.kr_date