from django.db import models
from account.models import User
# Create your models here.


class Customer(models.Model):

  name = models.CharField(max_length=150)
  contact_name = models.CharField(max_length=150)
  commercial_name = models.CharField(max_length=150)
  email = models.EmailField(unique=True)
  email_facturation = models.EmailField(unique=True, blank=True, null=True)
  phone = models.CharField(max_length=50, blank=True, null=True)
  address = models.CharField(max_length=150)
  city = models.CharField(max_length=32)
  zip_code = models.CharField(max_length=16)
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(User, on_delete=models.PROTECT)

  class Meta:
    verbose_name = "Customer"
    verbose_name_plural = "Customers"
    ordering = ['-created_at']
  
  def save(self, *args, **kwargs):
      # Si email_facturation n'est pas renseigné, on lui attribue la valeur de email
      if not self.email_facturation:
          self.email_facturation = self.email
      # Appelle la méthode save() parente pour enregistrer les données
      super().save(*args, **kwargs)

  def __str__(self):
    return self.name

class Invoice(models.Model):
   
  INVOICE_TYPE = (
    ("P", "PROFORMA"),
    ("R","RECU"),
    ("F","FACTURE")
    )

  customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
  created_by = models.ForeignKey(User, on_delete=models.PROTECT)
  invoice_date = models.DateTimeField(auto_now_add=True)
  montant = models.DecimalField(max_digits=100, decimal_places=2)
  last_update = models.DateTimeField(auto_now=True, null=True, blank=True)
  paid = models.BooleanField(default=False)
  invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
  comment = models.TextField(null=True, max_length=500, blank=True)

  class Meta:
    verbose_name = "Invoice"
    verbose_name_plural = "Invoices"

  def __str__(self):
        # Représentation en chaîne de caractères
        return f"Invoice {self.id} - {self.customer.name} ({self.invoice_date.strftime('%Y-%m-%d')})"