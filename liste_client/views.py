from django.shortcuts import render, redirect # type: ignore
# from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def customers(request):
  return render(request, 'liste_client/liste_client.html')
