from django.contrib import admin

from .models import *

# Register your models here.
class AdminCustomer(admin.ModelAdmin):
  list_display = (
    'name',
    'contact_name', 
    'email',
    'email_facturation', 
    'phone', 
    'address',
    'city',
    'zip_code',
    'created_at',
    'created_by'
    )
  
admin.site.register(Customer, AdminCustomer)