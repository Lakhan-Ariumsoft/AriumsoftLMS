from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTP

class UserAdmin(BaseUserAdmin):
    # Define fields for the admin panel
    list_display = ('email', 'first_name',"first_name", 'is_active', 'is_staff', 'last_login')
    

class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at')
    search_fields = ('user', 'otp_code')
# Register models
admin.site.register(User, UserAdmin)
admin.site.register(OTP, OTPAdmin)
