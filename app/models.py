from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from campusbuy2_0 import settings
from cloudinary.models import CloudinaryField
from django.contrib.postgres.fields import ArrayField
from datetime import datetime, timedelta

import jwt

from campusbuy2_0.settings import SECRET_KEY


class School(models.Model):
    name = models.CharField(null=True, blank=True, max_length=500, unique=True)
    alias = models.CharField(null=False, blank=True, max_length=500, unique=True)
    state = models.CharField(blank=True, null=True, max_length=500)
    hotspots = ArrayField(
        models.CharField(max_length=200, blank=True), size=50, default=list)

    def __str__(self):
        return self.alias


class Category(models.Model):
    """Product category model class"""
    name = models.CharField(max_length=500, null=False, blank=False, unique=True)
    description = models.CharField(max_length=500, default="Default")

    image = CloudinaryField('image', null=True, blank=True)  # Special Cloudinary image Field

    date_created = models.DateTimeField(blank=False, default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']
        verbose_name = "category"
        verbose_name_plural = "categories"


class SubCategory(models.Model):
    """ A more precise  categorization of products posted"""
    name = models.CharField(max_length=500, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    # image = CloudinaryField('image')  # Special Cloudinary image Field

    date_created = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return f"Category: {self.category}" + f" -  {self.name}"

    class Meta:
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"


class User(AbstractUser):
    """ The general User model """
    first_name = models.CharField(null=True, blank=True, max_length=200)
    last_name = models.CharField(null=True, blank=True, max_length=200)
    fullname = models.CharField(null=True, blank=True, max_length=200)
    phone_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    email_authenticated = models.BooleanField(default=False)
    whatsapp_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    is_merchant = models.BooleanField(default=False)
    # confirmed_payment = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)  # many to one relationship
    date_created = models.DateField(blank=False, default=timezone.now)
    # subscription_expired = models.BooleanField(default=False)
    #
    # @property
    # def get_full_name(self):
    #     """
    #     This method is required by Django for things like handling emails.
    #     Typically this would be the user's first and last name. We're returning the user's fullname
    #     """
    #     return f'{self.first_name} {self.last_name}'

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        """
        return self._generate_jwt_token()

    def __str__(self):
        return self.first_name


class OnlineStore(models.Model):
    """
    Model class for online store of merchants
    """
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(null=True, blank=True, max_length=500)
    description = models.CharField(null=True, blank=True, max_length=1000)
    address = models.CharField(null=True, blank=True, max_length=1000)
    logo = CloudinaryField('image', null=True, blank=True)  # Special Cloudinary image Field
    ratings = models.FloatField(default=0, null=True, blank=True, max_length=5)
    published_date = models.DateTimeField(blank=False, default=timezone.now)

    def __str__(self):
        return f"{self.business_name} {self.owner.fullname}'s"


class Product(models.Model):
    HALL4 = 'HALL4'
    HALL3 = 'HALL3'
    HALL2 = 'HALL2'
    HALL1 = 'HALL1'
    MAIN_GATE = 'Main Gate'
    GREEN_PARK = 'Green Park'
    GTBANK = 'GTBANK'
    NAAS_GARDEN = 'NAAS Garden'
    PHYSICAL_SCIENCE_COMPLEX = 'Physical Science Complex'
    MEDICAL_SCIENCE_COMPLEX = 'Med Complex'
    BASEMENT = 'Basement'
    JUNE12 = 'JUNE12'
    ENGINEERING = 'Engineering Park'

    SCHOOL_HOT_SPOTS = [
        ('Uniben', (
            (HALL4, 'Hall4'),
            (HALL3, 'Hall3'),
            (HALL2, 'Hall2'),
            (HALL1, 'Hall1'),
            (MAIN_GATE, 'Main gate'),
            (GREEN_PARK, 'Green Park'),
            (GTBANK, 'GTBank Wifi Spot'),
            (NAAS_GARDEN, 'Naas Garden'),
            (PHYSICAL_SCIENCE_COMPLEX, 'Physical Science Complex'),
            (MEDICAL_SCIENCE_COMPLEX, 'Medical Science Complex'),
            (BASEMENT, 'Basement'),
            (JUNE12, 'June12'),
            (ENGINEERING, 'Engineering Park')
        )
         )
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    merchant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    online_store = models.ForeignKey(OnlineStore, on_delete=models.SET_NULL, null=True)
    image = CloudinaryField('image', )  # Special Cloudinary image Field
    dropoff_point = models.TextField(max_length=500, choices=SCHOOL_HOT_SPOTS, default=MAIN_GATE, blank=True)
    name = models.CharField(max_length=500, blank=False, null=False)  # product name
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    exchange = models.BooleanField(default=False)
    exchange_for = models.CharField(max_length=500, blank=True, null=True)
    views = models.IntegerField(default=0)
    published_date = models.DateTimeField(blank=False, default=timezone.now)

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return f"Photo {self.name}:{public_id}"

    def published(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-published_date']
        verbose_name = "product"
        verbose_name_plural = "products"


class Purchase(models.Model):
    """
    The purchase model for every transaction
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    date_created = models.DateTimeField(blank=False, default=timezone.now)
    last_updated = models.DateTimeField(blank=False, default=timezone.now)
