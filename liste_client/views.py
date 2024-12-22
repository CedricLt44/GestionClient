from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Customer

# Create your views here.
@login_required
def customers(request):
  customers = Customer.objects.filter(created_by=request.user)

  return render(request, 'liste_client/liste_client.html',{
    'customers': customers
  })


@login_required
def customer(request, pk):
  customer = Customer.objects.filter(created_by=request.user).get(pk=pk)

  return render (request, 'liste_client/liste_client.html', {
    'customer': customer
  })

@login_required
def add(request):
  if request.method == 'POST':
    
    try:
      # Récupération des données avec strip() pour enlever les espaces
      customer_data = {
          'name': request.POST.get('name', '').strip(),
          'contact_name': request.POST.get('contact_name', '').strip(),
          'commercial_name': request.POST.get('commercial_name', '').strip(),
          'email': request.POST.get('email', '').strip(),
          'email_facturation': request.POST.get('email_facturation', '').strip(),
          'phone': request.POST.get('phone', '').strip(),
          'address': request.POST.get('address', '').strip(),
          'city': request.POST.get('city', '').strip(),
          'zip_code': request.POST.get('zip_code', '').strip(),
          'created_by': request.user
      }
      # Validation des champs obligatoires
      required_fields = ['name', 'contact_name', 'email', 'address', 'city', 'zip_code']
      for field in required_fields:
          if not customer_data[field]:
              messages.error(request, f'Le champ {field} est obligatoire.')
              return render(request, 'liste_client/add_client.html', {'data': customer_data})

      # Création du client
      customer = Customer(**customer_data)
      customer.full_clean()  # Validation du modèle
      customer.save()

      messages.success(request, 'Client ajouté avec succès!')
      return redirect('liste_client:customers')  # Utiliser le nom de l'URL

    except ValidationError as e:
        # Gestion des erreurs de validation du modèle
        for field, errors in e.message_dict.items():
            for error in errors:
                messages.error(request, f'Erreur dans le champ {field}: {error}')
        return render(request, 'liste_client/add_client.html', {'data': customer_data})

    except Exception as e:
        messages.error(request, f'Une erreur est survenue: {str(e)}')
        return render(request, 'liste_client/add_client.html', {'data': customer_data})

  return render(request, 'liste_client/add_client.html')