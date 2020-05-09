from datetime import datetime, date
import inspect
import json

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from campusbuy2_0 import settings
from cloudinary.models import CloudinaryField


class School(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200, unique=True)
    alias = models.CharField(null=False, blank=True, max_length=200, unique=True)
    state = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.alias


class User(AbstractUser):
    first_name = models.CharField(null=False, blank=False, max_length=200)
    last_name = models.CharField(null=False, blank=False, max_length=200)
    phone_number = models.CharField(max_length=12, blank=False, null=False, unique=True)
    whatsapp_number = models.CharField(max_length=12, blank=False, null=False, unique=True)
    business_name = models.CharField(null=False, blank=False, max_length=200, unique=True)
    business_description = models.TextField(max_length=300)
    address = models.CharField(null=False, blank=False, max_length=200)
    confirmed_payment = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)  # many to one relationship
    date_created = models.DateField(blank=False, default=timezone.now)
    subscription_expired = models.BooleanField(default=False)

    def published(self):
        self.date_created = timezone.now()
        self.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Category(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, unique=True)
    details = models.CharField(max_length=100, default="Default")

    # category_logo = CloudinaryField('category_logo')  # Special Cloudinary image Field

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    merchant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # image = CloudinaryField('image')  # Special Cloudinary image Field

    name = models.CharField(max_length=70, blank=False, null=False)  # product name
    description = models.TextField(max_length=250)
    price = models.FloatField()
    views = models.IntegerField(default=0)
    published_date = models.DateTimeField(blank=False, default=timezone.now)

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.name, public_id)

    def published(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-published_date']
