from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.SmallIntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Invoices(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=255, null=True)
    vendor = models.CharField(max_length=255, null=True)
    products = models.ManyToManyField("Products", through="InvoiceProductsList")
    sale_date = models.DateField(null=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=9)


class InvoiceProductsList(models.Model):
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE, null=True)
    products = models.ForeignKey("Products", on_delete=models.CASCADE, null=True)
    qty = models.SmallIntegerField()




class Products(models.Model):
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(decimal_places=2, max_digits=9)
    basic_points = models.SmallIntegerField()
    category = models.CharField(max_length=128)

    def __str__(self):
        return self.name