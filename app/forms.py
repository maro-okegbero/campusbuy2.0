from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Product, School, User
from django.contrib.auth import get_user_model
from campusbuy2_0 import settings


class PostAdForm(ModelForm):
    school = forms.ModelChoiceField(empty_label="Select School", queryset=School.objects.all(),
                                    widget=forms.Select(attrs={'class': 'business__location'}),)

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'image',
                  'description', 'dropoff_point', 'school']
        labels = {
            'name': forms.TextInput(attrs={'id': 'product_name'}),
            'category': forms.Select(attrs={'id': 'product_category'}),
            'price': forms.NumberInput(attrs={'id': 'product_price'}),
            'description': forms.TextInput(attrs={'id': 'product_description'}),
            'image': forms.TextInput(attrs={'id': 'product_image'}),
            'dropoff_point': forms.Select(attrs={'id': 'dropoff_point'}),
        }


class RegisterMerchantForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="FirstName",
                                 widget=forms.TextInput(attrs={'id': 'first_name'}))
    last_name = forms.CharField(max_length=30, required=True, label="LastName",
                                widget=forms.TextInput(attrs={'id': 'last_name'}))
    email = forms.EmailField(max_length=254, required=True, label="Email",
                             widget=forms.EmailInput(attrs={'id': 'email'}))

    business_name = forms.CharField(max_length=30, required=True, label="BusinessName",
                                    widget=forms.TextInput(attrs={'id': 'business_name'}))
    address = forms.CharField(max_length=30, required=True, label="Address",
                              widget=forms.TextInput(attrs={'id': 'address'}))
    username = forms.CharField(max_length=30, required=True, label="Username",
                               widget=forms.TextInput(attrs={'id': 'username'}))
    school = forms.ModelChoiceField(empty_label="Select School", queryset=School.objects.all(),
                                    widget=forms.Select(attrs={'class': 'business__location'}))
    business_description = forms.CharField(max_length=300, required=True, label="Business Description",
                                           widget=forms.Textarea(attrs={'id': 'description'}))
    phone_number = forms.CharField(max_length=16, required=True, label="Phone Number",
                                   widget=forms.TextInput(attrs={'id': 'phone_number'}))
    whatsapp_number = forms.CharField(max_length=16, required=True, label="Whatsapp Number",
                                      widget=forms.TextInput(attrs={'id': 'whatsapp_number'}))

    class Meta:
        User = get_user_model()
        model = User
        fields = ['username', 'first_name', 'last_name', 'business_name', 'address', 'business_description',
                  'phone_number', 'whatsapp_number', 'email', 'school',
                  'password1', 'password2']


class LoginMerchantForm(forms.Form):
    username = forms.CharField(max_length=30, required=True,
                               widget=forms.TextInput(attrs={'class': "form--input", "id": "login-email"}),
                               label="Username")
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(
        attrs={'class': "form--input eye--password", 'id': "login-password"}), label="Password")


class SchoolSelectForm(forms.Form):
    school = forms.ModelChoiceField(required=False, empty_label="Select School", queryset=School.objects.all())


class MerchantPersonalInformationForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False,
                                 widget=forms.TextInput(attrs={'class': "form--input", "id": "first-name"}),
                                 label="First Name")
    last_name = forms.CharField(max_length=30, required=False,
                                widget=forms.TextInput(attrs={'class': "form--input", "id": "last-name"}),
                                label="Last Name")
    phone_number = forms.CharField(max_length=12, required=False,
                                   widget=forms.TextInput(attrs={'class': "form--input", "id": "tel"}),
                                   label="Phone Number")
    whatsapp_number = forms.CharField(max_length=12, required=False,
                                      widget=forms.TextInput(attrs={'class': "form--input", "id": "whatsapp-tel"}),
                                      label="Whatsapp Number")


class MerchantBusinessDetailsForm(forms.Form):
    business_name = forms.CharField(max_length=300, required=False,
                                    widget=forms.TextInput(attrs={'class': "form--input", "id": "business-name"}),
                                    label="Business Name")
    business_description = forms.CharField(max_length=300, required=False,
                                           widget=forms.Textarea(
                                               attrs={'class': "form--input", "id": "business-desc", "rows": "5"}),
                                           label="Business Description")


class MerchantLoginDetailsForm(forms.Form):
    username = forms.CharField(max_length=30, required=False,
                               widget=forms.TextInput(attrs={'class': "form--input", "id": "login-email"}),
                               label="Username")

    email = forms.CharField(max_length=30, required=False,
                            widget=forms.EmailInput(
                                attrs={'class': "form--input", "id": "reg-email"}),
                            label="Email")

    password1 = forms.CharField(max_length=30, required=False,
                                widget=forms.PasswordInput(
                                    attrs={'class': "form--input eye--password", "id": "reg-current-password1"}),
                                label="Password1")

    password2 = forms.CharField(max_length=30, required=False,
                                widget=forms.PasswordInput(

                                    attrs={'class': "form--input eye--password", "id": "reg-current-password2"}),
                                label="Password2")
