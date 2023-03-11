import csv
from Loyalty_program_app.models import Products, Invoices, InvoiceProductsList, UserProfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Imports sells data to loyalty porgram db"

    def handle(self, *args, **kwargs):
        with open('data.csv') as file:
            reader = csv.reader(file, delimiter=',')
            uniqueinvoice = []

            for row in reader:
                invoice_number = row[0]
                vendor = row[1]
                sale_date = row[2]
                total_price = row[3]
                user_id = row[4]
                product_id = row[5]
                qty = row[6]

                if invoice_number not in uniqueinvoice:
                    uniqueinvoice.append(invoice_number)
                    invoice = Invoices.objects.get_or_create(
                        invoice_number=invoice_number,
                        vendor=vendor,
                        sale_date=sale_date,
                        total_price=total_price,
                        user_id=user_id
                    )

                invoiceproductlist = InvoiceProductsList.objects.get_or_create(
                    invoice=Invoices.objects.latest('id'),
                    products=Products.objects.get(pk=product_id),
                    qty=qty
                )

                user = UserProfile.objects.get(pk=user_id)
                product = Products.objects.get(pk=product_id)
                user.points += product.basic_points * int(qty)
                user.save()