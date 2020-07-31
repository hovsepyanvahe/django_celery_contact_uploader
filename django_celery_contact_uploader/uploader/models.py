from django.db import models
from phone_field import PhoneField


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneField()
    email = models.EmailField(max_length=100)

    def __str__(self):
        return '{} - ({}) - {}'.format(self.name, self.phone, self.email)


class File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.name
