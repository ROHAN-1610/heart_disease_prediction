from django.contrib import admin

# Register your models here.
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'dob', 'hospital_name')
    search_fields = ('user__username', 'phone_number', 'hospital_name')

admin.site.register(UserProfile, UserProfileAdmin)