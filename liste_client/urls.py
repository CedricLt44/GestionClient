from django.urls import path

from . import views

app_name = 'liste_client'

urlpatterns = [
  path('customers/',views.customers, name='customers'),
]