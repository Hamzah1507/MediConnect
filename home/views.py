from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SignupUser
from django.contrib.auth.hashers import make_password

def landing_page(request):
    return render(request, "landing.html")

# ✅ This is your single Sign Up page (signin.html)
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # hash password before saving (secure storage)
            SignupUser.objects.create(
                name=name,
                email=email,
                password=password
            )
            messages.success(request, "User registered successfully!")
            return redirect("signup") 
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "signin.html") 
