from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.site_header = 'CAMPUSBUY god MODE'
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(School)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SubCategory)

