from Loyalty_program_app.models import Products, Invoices, InvoiceProductsList, UserProfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Counting points of new invoices"

    def handle(self, *args, **kwargs):
        notcountedinvoices = Invoices.objects.filter(countpoints=False)
        for invoice in notcountedinvoices:
            invoiceproductlist = InvoiceProductsList.objects.filter(invoice=invoice.pk)
            for item in invoiceproductlist:
                qty = item.qty
                productbasicpoints = item.products.basic_points
                sumofpoints = int(qty * productbasicpoints)


                invoice.points += sumofpoints
                invoice.save()

            user = UserProfile.objects.get(pk=invoice.user.pk)
            user.points += invoice.points
            user.save()
            invoice.countpoints = True
            invoice.save()
