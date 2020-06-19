from django.contrib import admin

# Register your models here.
from .models import krdaily, Country, World_daily, kr_region

admin.site.register(krdaily)
admin.site.register(Country)
admin.site.register(World_daily)
admin.site.register(kr_region)