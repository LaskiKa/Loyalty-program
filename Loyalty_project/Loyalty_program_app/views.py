from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from Loyalty_program_app.models import Products, InvoiceProductsList, UserProfile, Invoices

from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.list import ListView


# Create your views here.
class Base(View):
    def get(self, request):
        products = Products.objects.all()
        return render(request,
                      'Loyalty_program_app/base.html',
                      {'products': products})


class UserMainSite(LoginRequiredMixin, View):
    def get(self, request):
        userpoints = UserProfile.objects.get(user=self.request.user).points
        return render(request,
                      "Loyalty_program_app/user-main-site.html",
                      context={'userpoints': userpoints})


class ProductAddView(LoginRequiredMixin, CreateView):
    model = Products
    fields = ["name", "unit_price", "basic_points", "category"]
    success_url = "/base/"  # do poprawki + zmiana tempaltki

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Products
    fields = ["name", "unit_price", "basic_points", "category"]
    success_url = "/base/"
    template_name_suffix = '_update_form'


class InvoiceListView(LoginRequiredMixin, View):

    def get(self, request):
        userinvoices = Invoices.objects.filter(user=self.request.user.id).order_by('-sale_date')
        for a in userinvoices:
            print(a.invoice_number)
        userpoints = UserProfile.objects.get(user=self.request.user).points
        pointsperinvoice = {}

        for invoice in userinvoices:
            invoicepoints = 0
            invoiceproductlist = InvoiceProductsList.objects.filter(invoice=invoice.pk)
            for item in invoiceproductlist:
                qty = item.qty
                basic_points = item.products.basic_points
                invoicepoints += int(qty * basic_points)

            pointsperinvoice[invoice.id] = invoicepoints

        return render(request,
                      'Loyalty_program_app/invoices_list.html',
                      context={"userinvoices": userinvoices,
                               "userpoints": userpoints,
                               "pointsperinvoice": pointsperinvoice.items()})


class InvoiceDetaliView(LoginRequiredMixin, View):

    def get(self, request, pk):
        pointsperprod = {}
        sumpointsofinvoice = 0
        invoice = Invoices.objects.get(pk=pk)
        invoiceproductlist = InvoiceProductsList.objects.filter(invoice=pk)

        for item in invoiceproductlist:
            qty = item.qty
            basic_points = item.products.basic_points
            pointsperprod[item.id] = int(qty * basic_points)
            sumpointsofinvoice += int(qty * basic_points)
        return render(request,
                      'Loyalty_program_app/invoices_detail.html',
                      context={'invoiceproductlist': invoiceproductlist,
                               'invoice': invoice,
                               'pointsperprod': pointsperprod.items(),
                               'sumpointsofinvoice': sumpointsofinvoice})


class InvoiceAddView(LoginRequiredMixin, CreateView):
    model = Invoices
    fields = ["invoice_number", "vendor", "products", "sale_date", "total_price"]
    success_url = HttpResponseRedirect('invoices-list')


class PurchesSummary(LoginRequiredMixin, View):
    """Zestawienie zakupów z podziałem na lata"""

    def get(self, request):
        userinvoices = Invoices.objects.filter(user=self.request.user.id).order_by('-sale_date')
        userpoints = UserProfile.objects.get(user=self.request.user).points
        products = Products.objects.all()
        productsummary = {}

        for product in products:
            productsummary[product.name] = [0, 0]

        for invoice in userinvoices:
            invoiceproductlist = InvoiceProductsList.objects.filter(invoice=invoice.pk)

            for item in invoiceproductlist:
                qty = item.qty
                productpoints = 0
                basic_points = item.products.basic_points
                productpoints += int(qty * basic_points)

                productsummary[item.products.name][0] += qty
                productsummary[item.products.name][1] += productpoints

                print(item.products.name, productsummary[item.products.name][0], productsummary[item.products.name][1] )

        return render(request,
                      'Loyalty_program_app/purchase_summary.html',
                      context={"userpoints": userpoints,
                               "productsummary": productsummary.items()})
