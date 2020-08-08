from django.urls import path
from .views import login_user, register_user, category_handler

urlpatterns = [
    path('login', login_user, name="login"),
    path('signup', register_user, name="login"),
    path('categories', category_handler, name="categories"),
    path('categories/<pk>', category_handler, name="categories"),
]