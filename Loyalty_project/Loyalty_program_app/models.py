from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    password = models.CharField(max_length=64)
    invoices = models.ForeignKey("Invoices", on_delete=models.CASCADE)
    points = models.SmallIntegerField(default=0)


class Invoices(models.Model):
    invoice_number = models.CharField(max_length=255)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.CharField(max_length=255, blank=False)
    products = models.ManyToManyField("Products", through="InvoiceProductsList")
    sale_date = models.DateField(blank=False)
    total_price = models.DecimalField(decimal_places=2)


class InvoiceProductsList(models.Model):
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    products = models.ForeignKey("Products", on_delete=models.CASCADE)
    qty = models.SmallIntegerField()


class Products(models.Model):
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(decimal_places=2)
    basic_points = models.SmallIntegerField()
