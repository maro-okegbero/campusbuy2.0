from django.shortcuts import render


def homepage(request):
    """
    This view is responsible for displaying the contents of the homepage
    """
    return render(request, "campusbuy2_0/landing.html")

