from django.urls import path, include
from uniben.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('accounts/', include('django.contrib.auth.urls')),

    path('', homepage, name='homepage'),

    path('<str:school_name>/', homepage, name='school_specific'),

    path('login&register', login_register, name='login/register_merchant'),

    path('profile', merchant_profile, name='profile'),

    path('<school_name>/profile', merchant_profile, name='school_specific_profile'),

    # path('login', login_merchant, name='login'),

    path('post_product', post_products, name='post_products'),

    path('search', search, name='search'),

    path('about_us', about_us, name='about'),

    path('contact_us', contact_us, name='contact'),

    path('faq', faq, name='faq'),

    path('<school_name>/faq', faq, name='school_specific_faq'),

    path('logout', signout, name='logout'),

    path('ajax/validate_username/', validate_username, name='validate_username'),

    path('<business_name>/product_stats/<pk>', product_stat, name="product_stat"),

    path('product_edit/<pk>', product_edit, name="product_edit"),

    path('product_delete/<pk>', product_delete, name="product_delete"),

    path('all_products', view_all_products, name='view_all_products'),

    path('shop/<business_name>', merchant_shop, name='shop'),

    path('<category_name>/<int:pk>', single_product, name='product_detail'),

    path('<school_name>/<category_name>/<int:pk>', single_product, name='product_detail_school_specific'),

    path('<school_name>/all_products', view_all_products, name='view_all_products_school_specific'),

    path('<school_name>/<category_name>', view_products, name='view_products_school_specific'),

    path('<category_name>', view_products, name='view_products'),

    path('<school_name>/shop/<business_name>', merchant_shop, name='shop_school_specific'),
]
