from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from campusbuy2_0 import settings
from cloudinary.models import CloudinaryField
from django.contrib.postgres.fields import ArrayField


class School(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200, unique=True)
    alias = models.CharField(null=False, blank=True, max_length=200, unique=True)
    state = models.CharField(blank=True, null=True, max_length=200)
    hotspots = ArrayField(
        models.CharField(max_length=200, blank=True), size=50, default=list)

    def __str__(self):
        return self.alias


class User(AbstractUser):
    """ The User model for both merchants and regular users"""
    first_name = models.CharField(null=True, blank=True, max_length=200)
    last_name = models.CharField(null=True, blank=True, max_length=200)
    phone_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    whatsapp_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    is_merchant = models.BooleanField(default=True)
    business_name = models.CharField(null=True, blank=True, max_length=200, unique=True)
    business_description = models.TextField(max_length=300)
    address = models.CharField(null=True, blank=True, max_length=200)
    confirmed_payment = models.BooleanField(default=False, )
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)  # many to one relationship
    rating = models.FloatField(default=0, null=True)
    date_created = models.DateField(blank=False, default=timezone.now)
    subscription_expired = models.BooleanField(default=False)

    def published(self):
        self.date_created = timezone.now()
        self.save()

    def __str__(self):
        return self.business_name


class Category(models.Model):
    """Product category model class"""
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    details = models.CharField(max_length=200, default="Default")

    # image = CloudinaryField('image')  # Special Cloudinary image Field

    date_created = models.DateTimeField(blank=False, default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']
        verbose_name = "category"
        verbose_name_plural = "categories"


class SubCategory(models.Model):
    """ A more precise  categorization of products posted"""
    name = models.CharField(max_length=100, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    # image = CloudinaryField('image')  # Special Cloudinary image Field

    date_created = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return f"Category: {self.category}" + f" -  {self.name}"

    class Meta:
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"


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
         ),
        # ('Video', (
        #     ('vhs', 'VHS Tape'),
        #     ('dvd', 'DVD'),
        # )
        #  ),
    ]
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    merchant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    image = CloudinaryField('image')  # Special Cloudinary image Field
    dropoff_point = models.TextField(max_length=250, choices=SCHOOL_HOT_SPOTS, default=MAIN_GATE, blank=True)
    name = models.CharField(max_length=70, blank=False, null=False)  # product name
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    exchange = models.BooleanField(default=False)
    exchange_for = models.CharField(max_length=70, blank=True, null=True)
    views = models.IntegerField(default=0)
    published_date = models.DateTimeField(blank=False, default=timezone.now)

    def __unsicode__(self):
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
        verbose_name = "product"
        verbose_name_plural = "products"

