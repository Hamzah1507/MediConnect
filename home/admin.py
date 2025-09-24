from django.contrib import admin
from .models import SignupUser, Medicine # Import both models

# Register your models here.
admin.site.register(SignupUser)
admin.site.register(Medicine)