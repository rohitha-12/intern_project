from django.contrib import admin
from .models import CustomUser, EmailOTP, CompanyEmail

admin.site.register(CustomUser)
admin.site.register(EmailOTP)
admin.site.register(CompanyEmail)

# Register your models here.
