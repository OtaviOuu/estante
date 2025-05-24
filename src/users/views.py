from django.shortcuts import render

# Create your views here.


def register(request):
    """
    Render the register page.
    """
    return render(request, "users/register.html")


def login(request):
    """
    Render the login page.
    """
    return render(request, "users/login.html")
