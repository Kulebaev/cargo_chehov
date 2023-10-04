from django.contrib import admin
from .models import Car, Subscriber, CarImage

admin.site.register(Car)
admin.site.register(CarImage)
admin.site.register(Subscriber)
