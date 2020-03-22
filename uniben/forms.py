from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Product, School
from django.contrib.auth import get_user_model
from campusbuy2_0 import settings


class PostAdForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = ['category', 'name', 'price',
        #           'description', 'image']
        fields = ['category', 'name', 'price',
                  'description']


class RegisterMerchant(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label="FirstName", widget=forms.TextInput(attrs={'id': 'first_name'}))
    last_name = forms.CharField(max_length=30, required=False, label="LastName", widget=forms.TextInput(attrs={'id': 'last_name'}))
    email = forms.EmailField(max_length=254,  label="Email", widget=forms.TextInput(attrs={'id': 'email'}))
    business_name = forms.CharField(max_length=30, required=False, label="BusinessName", widget=forms.TextInput(attrs={'id': 'business_name'}))
    address = forms.CharField(max_length=30, required=False, label="Address", widget=forms.TextInput(attrs={'id': 'address'}))
    username = forms.CharField(max_length=30, required=True, label="Username", widget=forms.TextInput(attrs={'id': 'username'}))
    school = forms.ModelChoiceField(empty_label="Select School", queryset=School.objects.all(),
                                    widget=forms.Select(attrs={'class': 'business__location'}))
    business_description = forms.CharField(max_length=300, required=True, label="Business Description",
                                           widget=forms.Textarea(attrs={'id': 'description'}))
    phone_number = forms.CharField(max_length=16, required=True, label="Phone Number", widget=forms.TextInput(attrs={'id': 'phone_number'}))
    whatsapp_number = forms.CharField(max_length=16, required=True, label="Whatsapp Number", widget=forms.TextInput(attrs={'id': 'whatsapp_number'}))

    class Meta:
        User = get_user_model()
        model = User
        fields = ['username', 'first_name', 'last_name', 'business_name', 'address', 'business_description',
                  'phone_number', 'whatsapp_number', 'email', 'school',
                  'password1', 'password2']


class LoginMerchant(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': "form--input", "id": "login-email"}), label="Username")
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': "form--input eye--password", 'id': "login-password"}), label="Password")


class SelectSchool(forms.Form):
    school = forms.ModelChoiceField(empty_label="Select School", queryset=School.objects.all())
