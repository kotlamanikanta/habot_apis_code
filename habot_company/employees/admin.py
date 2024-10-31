# admin.py
from django.contrib import admin
from .models import Employee

# Define EmployeeAdmin if you need customization
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name']  # Example fields

# Register Employee model with EmployeeAdmin
admin.site.register(Employee, EmployeeAdmin)
