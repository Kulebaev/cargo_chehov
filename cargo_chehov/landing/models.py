from django.db import models

class Car(models.Model):
    title = models.CharField(max_length=200)
    image = models.ManyToManyField('CarImage', blank=True)
    descriptions = models.CharField(max_length=400)

    def __str__(self):
        return self.title
    
class CarImage(models.Model):
    file = models.FileField(upload_to='car_images/')


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email