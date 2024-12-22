from django.db import models
from account.models import User
from django.core.validators import RegexValidator
# Create your models here.


class Customer(models.Model):

  name = models.CharField(max_length=150, verbose_name="Company Name")
  contact_name = models.CharField(max_length=150, verbose_name="Contact person")
  commercial_name = models.CharField(max_length=150, verbose_name="Commercial Name")
  email = models.EmailField(unique=True, verbose_name="Primary Email")
  email_facturation = models.EmailField(unique=True, blank=True, null=True, verbose_name="email facturation")
  phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^(?:\+33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$',
                message="Le numéro de téléphone doit être au format : '+33 6 12 34 56 78' ou '06 12 34 56 78'"
            )
        ]
    )
  address = models.CharField(max_length=150)
  city = models.CharField(max_length=32)
  zip_code = models.CharField(max_length=16)
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="customers_created")

  class Meta:
    verbose_name = "Customer"
    verbose_name_plural = "Customers"
    ordering = ['-created_at']
    indexes = [
    models.Index(fields=['name']),
    models.Index(fields=['email']),
]

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
  created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='invoices_created')
  invoice_date = models.DateTimeField(auto_now_add=True)
  montant = models.DecimalField(max_digits=100, decimal_places=2)
  last_update = models.DateTimeField(auto_now=True, null=True, blank=True)
  paid = models.BooleanField(default=False)
  invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
  comment = models.TextField(null=True, max_length=500, blank=True)

  class Meta:
    verbose_name = "Invoice"
    verbose_name_plural = "Invoices"
    ordering = ['-invoice_date']
    indexes = [
      models.Index(fields=['invoice_date']),
      models.Index(fields=['customer']),
      models.Index(fields=['paid']),
]

  def __str__(self):
        # Représentation en chaîne de caractères
        return f"Invoice {self.id} - {self.customer.name} ({self.invoice_date.strftime('%Y-%m-%d')})"