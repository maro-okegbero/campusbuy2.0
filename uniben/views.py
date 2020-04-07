"""
Author: Maro Okegbero
Date : 15th of February 2020
"""
from datetime import datetime

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'username_exists': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def paginator(object_set, segments, request):
    """
    spreads object_list across  pages

    :param object_set:
    :param segments:
    :param request
    return object_list
    """

    page = request.GET.get('page', 1)
    segmentor = Paginator(object_set, segments)
    try:
        object_list = segmentor.page(page)
    except PageNotAnInteger:
        object_list = segmentor.page(1)
    except EmptyPage:
        object_list = segmentor.page(segmentor.num_pages)
    return object_list


def landing_page_redirect(request):
    return redirect(homepage)


def about_us(request):
    """Renders the about us page"""
    return render(request, 'campusbuy2_0/about.html')


def faq(request, school_name=None):
    context = {'school_name_for_url': school_name}
    return render(request, 'campusbuy2_0/faq.html', context)


def contact_us(request):
    """Renders the about us page"""
    return render(request, 'campusbuy2_0/contact.html')


def homepage(request, school_name=None):
    """
    This view is responsible for rendering the categories on the homepage
    :param request:
    :param request:
    :param school_name:
    :return:
    """
    supported_schools = ["Uniben"]
    if school_name in supported_schools or not school_name:
        categories = Category.objects.all()  # get all the categories
        products = Product.objects.filter(school__alias=school_name).all()[
                   :5] if school_name else Product.objects.all()[:5]
        print(products.all(), "all Products")
        if request.method == "GET":
            form = SelectschoolForm(request.GET)
            if form.is_valid():
                print(form.cleaned_data.get("school"), "SCHOOOLLLL")
                form_school_name = form.cleaned_data.get("school")
                return redirect(reverse('school_specific', args=[form_school_name]))
        else:
            form = SelectschoolForm()
        context = {'categories': categories,
                   'school_name_for_url': school_name,
                   'products': products,
                   'value': datetime.now(),
                   'form': form
                   }

        return render(request, 'campusbuy2_0/index.html', context)
    else:
        return render(request, 'campusbuy2_0/no _support.html', {'school_name': school_name})


def view_products(request, category_name, school_name=None):
    """
    This view displays all the products in a given category of a named school

    :param request:
    :param category_name:
    :param school_name:
    """
    try:
        category = Category.objects.get(name=category_name)
        # schools = {
        #     "uniben": "University Of Benin"
        # }
        my_list = category.product_set.filter(
            school__alias=school_name) if school_name else category.product_set.all()
        product_list = paginator(my_list, 4, request)
        context = {'category': category_name,
                   'products': product_list,
                   'school_name': school_name,
                   'school_name_for_url': school_name,
                   'value': datetime.now()
                   }
        return render(request, 'campusbuy2_0/products.html', context)

    except Category.DoesNotExist as e:
        return handler404(request, e)


def view_all_products(request, school_name=None):
    """This displays all the products in the system of a named school"""

    all_products = Product.objects.filter(
        school__alias=school_name).defer('school', 'merchant',
                                         'description') if school_name else Product.objects.all().defer('school',
                                                                                                        'merchant',
                                                                                                        'description')
    context = {"all_products": all_products, 'school_name': school_name,
               'school_name_for_url': school_name,
               'value': datetime.now()
               } if school_name else {"all_products": all_products, 'value': datetime.now()}
    return render(request, 'campusbuy2_0/all_products.html', context)


@login_required(login_url='/login&register')
def product_stat(request, business_name, pk):
    """handles rendering of the products statistics"""
    product = Product.objects.get(pk=pk)
    if request.user.username == product.merchant.username:
        context = {'product': product, 'business_name': business_name}
        return render(request, 'campusbuy2_0/product_stat.html', context)
    else:
        return render(request, 'campusbuy2_0/unauthorized.html')


# def delete_product(request, pk)


@login_required(login_url='/login&register')
def post_products(request):
    """
    This view handles the posting of products. It requires that the user be logged in
    """
    if request.method == "POST":
        form = PostAdForm(request.POST, request.FILES, auto_id=True)
        if form.is_valid():
            post = form.save()
            post.published_date = timezone.now()
            post.merchant = request.user
            post.school = request.user.school
            school = request.user.school
            print(request.user.school, "SCHOOL ++++++++++++++++++HURRAY")
            post.save()
            return redirect(reverse('view_products_school_specific', kwargs={'school_name': request.user.school.alias,
                                                                             'category_name': post.category.name}))

    else:

        form = PostAdForm()
    return render(request, 'campusbuy2_0/new_product.html', {'form': form})


def single_product(request, pk, category_name=None, school_name=None):
    """
    This view handles the rendering of just a product
    """
    try:
        product = Product.objects.select_related('category', 'merchant').get(pk=pk)
        product.views += 1
        product.save()
        name = product.name
        category_name = product.category.name
        merchant = product.merchant
        similar_products = Product.objects.filter(Q(category=product.category.pk)
                                                  & Q(name__contains=name)).defer('school', 'merchant', 'description')[
                           :5]  # combined queryset
        other_products_from_merchant = Product.objects.filter(merchant__id=merchant.id).defer('school', 'merchant',
                                                                                              'description')[:5]
        # schools = {
        #     "uniben": "University Of Benin"
        # }
        context = {'product': product,
                   'category_name': category_name,
                   'school_name': school_name,
                   'school_name_for_url': school_name,
                   'value': datetime.now(),
                   'similar_products': similar_products,
                   'other_products_from_merchant': other_products_from_merchant
                   }
        return render(request, 'campusbuy2_0/product_detail.html', context)
    except Exception as e:
        return handler404(request, e)


@login_required(login_url='/login&register')
def merchant_profile(request, school_name=None):
    user = request.user
    merchant = User.objects.get(first_name=user.first_name)
    print(merchant.business_name)
    products_set = merchant.product_set.all().defer('school', 'merchant', 'description')
    products = paginator(products_set, 5, request)

    if request.method == "GET":
        # the bounded forms
        personal_information_form = PersonalInformationForm(request.GET)
        business_detail_form = BusinessDetailsForm(request.GET)
        login_details_form = LoginDetailsForm(request.GET)
        check = lambda form_value, normal_value: form_value == normal_value and len(
            form_value) != 0  # lambda function to validate the new value

        if personal_information_form.is_valid():

            first_name = personal_information_form.cleaned_data.get("first_name")
            merchant.first_name = first_name if check(first_name, user.first_name) else user.first_name

            last_name = personal_information_form.cleaned_data.get("last_name")
            merchant.last_name = last_name if check(last_name, user.last_name) else user.last_name

            phone_number = personal_information_form.cleaned_data.get("phone_number")
            merchant.phone_number = phone_number if check(phone_number, user.phone_number) else user.phone_number

            whatsapp_number = personal_information_form.cleaned_data.get("whatsapp_number")
            merchant.whatsapp_number = whatsapp_number if check(whatsapp_number,
                                                                user.whatsapp_number) else user.whatsapp_number
            merchant.save()

        elif business_detail_form.is_valid():

            business_name = business_detail_form.cleaned_data.get("business_name")
            merchant.business_name = business_name if check(business_name, user.business_name) else user.business_name

            business_description = business_detail_form.cleaned_data.get("business_description")
            merchant.business_description = business_description if check(business_description,
                                                                          user.business_description) else user.business_description

        elif login_details_form.is_valid():

            username = login_details_form.cleaned_data.get("username")
            merchant.username = username if check(username, user.username) else user.username

            password1 = login_details_form.cleaned_data.get("password1")
            password2 = login_details_form.cleaned_data.get("password2")
            if password1 == password2:
                merchant.set_password(password1)

        merchant.save()
    else:
        personal_info_data = dict(email=user.email, first_name=user.first_name, last_name=user.last_name,
                                  phone_number=user.phone_number, whatsapp_number=user.whatsapp)

        business_detail_data = dict(business_name=user.business_name, business_description=user.business_description)

        login_details_data = dict()

        # the bounded forms
        personal_information_form = PersonalInformationForm(data=personal_info_data)
        business_detail_form = BusinessDetailsForm(data=business_detail_data)
        login_details_form = LoginDetailsForm(data=login_details_data)

    context = {"products": products,
               "school_name_for_url": school_name,
               "personal_information_form": personal_information_form,
               "business_detail_form": business_detail_form,
               "login_details_form": login_details_form
               }

    return render(request, 'campusbuy2_0/profile.html', context)


def merchant_shop(request, business_name, school_name=None):
    """
    This shows all the product posts of a particular merchant

    """
    try:
        merchant = User.objects.get(business_name=business_name)
        products_set = merchant.product_set.defer('school', 'merchant', 'description')
        products = paginator(products_set, 5, request)
        school_name = merchant.school.alias
        context = {'products': products, 'business_name': business_name,
                   'merchant': merchant,
                   'school_name': school_name,
                   'school_name_for_url': school_name,
                   'value': datetime.now()
                   }

        return render(request, 'campusbuy2_0/shop.html', context)

    except User.DoesNotExist as e:
        return handler404(request, e)


def login_register(request):
    if request.user.is_authenticated:
        return redirect(merchant_profile)
    if request.method == "POST":
        registration_form = RegisterMerchantForm(request.POST, request.FILES, auto_id=True)
        login_form = LoginMerchantForm(request.POST, auto_id=True)

        if registration_form.is_valid():

            registration_form.save()

            username = registration_form.cleaned_data.get('username')

            raw_password = registration_form.cleaned_data.get('password1')

            merchant = authenticate(username=username, password=raw_password)

            login(request, merchant)
            return redirect(merchant_profile)

        elif login_form.is_valid():

            username = request.POST.get("username", "")

            password = request.POST.get("password", "")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(merchant_profile)
            else:
                context = {'error': "The username or password is wrong",
                           'login_form': login_form,
                           'registration_form': registration_form}
                return render(request, 'campusbuy2_0/login_register.html', context)

    else:
        registration_form = RegisterMerchantForm(auto_id=True)
        login_form = LoginMerchantForm(auto_id=False)

    context = {
        'login_form': login_form,
        'registration_form': registration_form}
    return render(request, 'campusbuy2_0/login_register.html', context)


# def login_merchant(request):
#     """
#     This view handles authorization and authentication
#     """
#     if request.method == 'POST':
#         form = LoginMerchant(request.POST)
#         if form.is_valid():
#             username = request.POST.get("username", "")
#             password = request.POST.get("password", "")
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(merchant_profile)
#             else:
#                 context = {'error': "The username or password is wrong",
#                            'form': form}
#                 return render(request, 'campusbuy2_0/login_register.html', context)
#
#     else:
#         form = LoginMerchant()
#
#     return render(request, 'campusbuy2_0/login_register.html', {'form': form})
#

def search(request, school_name=None):
    """
    This view is responsible for handling search
    """
    query = request.GET.get('q')
    results = []
    print(query, "Ze Querrryyyyyy")
    no_school_query = Product.objects.annotate(search=SearchVector('name', 'description', )).filter(
        search=query).defer('school', 'merchant', 'description')
    school_exists_query = Product.objects.annotate(search=SearchVector('name', 'description', )).filter(
        search=query).defer('school', 'merchant', 'description').filter(school__alias=school_name)
    if query:
        results_set = school_exists_query if school_name else no_school_query
        results = paginator(results_set, 5, request)
        print(results.object_list, "RESULTS HALLELUYA")

    return render(request, 'campusbuy2_0/search.html', {'results': results})


def signout(request):
    """wipe out session data for the current request"""
    logout(request)
    return redirect(login_register)


def handler404(request, exception, template_name="404_Error.html"):
    """
    This view handles the custom display of the 404 page
    """
    response = render(request, "campusbuy2_0/404_Error.html")
    response.status_code = 404
    return response
