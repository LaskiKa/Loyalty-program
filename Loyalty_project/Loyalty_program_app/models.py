from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField(default=0)
    nip = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Invoices(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    purchaser_nip = models.CharField(max_length=10, null=True)
    invoice_number = models.CharField(max_length=255, null=True)
    vendor = models.CharField(max_length=255, null=True)
    products = models.ManyToManyField("Products", through="InvoiceProductsList")
    sale_date = models.DateField(null=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=9)
    countpoints = models.BooleanField(default=False)
    points = models.IntegerField(default=0)


class InvoiceProductsList(models.Model):
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE, null=True)
    products = models.ForeignKey("Products", on_delete=models.CASCADE, null=True)
    qty = models.IntegerField()


class Products(models.Model):
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(decimal_places=2, max_digits=9)
    basic_points = models.IntegerField()
    category = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Prizes(models.Model):
    name = models.CharField(max_length=255)
    points_value = models.IntegerField()
    available_quantity = models.SmallIntegerField()
    prize_description = models.TextField()
    rating = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Carts(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    prize = models.ManyToManyField(Prizes, through='CartItems')
    order_date = models.DateField()


class CartItems(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prizes, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class PrizeOpinions(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    prize = models.ManyToManyField(Prizes)
    opinion = models.TextField()
    rating = models.IntegerField()
