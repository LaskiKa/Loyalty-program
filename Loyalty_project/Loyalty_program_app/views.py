from django.contrib.auth.mixins import LoginRequiredMixin
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
        return render(request,
                      "Loyalty_program_app/user-main-site.html")


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


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoices
    paginate_by = 30

    def get_queryset(self):
        # userprofile = UserProfile.objects.filter(user=self.request.user.id)
        userinvoices = Invoices.objects.filter(user=self.request.user.id)
        return userinvoices


class InvoiceDetaliView(LoginRequiredMixin, View):

    def get(self, request, pk):
        pointsperprod = {}
        sumofpoints = 0
        invoice = Invoices.objects.get(pk=pk)
        invoiceproductlist = InvoiceProductsList.objects.filter(invoice=pk)

        for item in invoiceproductlist:
            qty = item.qty
            basic_points = item.products.basic_points
            pointsperprod[item.id] = int(qty * basic_points)
            sumofpoints += int(qty * basic_points)
        return render(request,
                      'Loyalty_program_app/invoices_detail.html',
                      context={'invoiceproductlist': invoiceproductlist,
                               'invoice': invoice,
                               'pointsperprod': pointsperprod.items(),
                               'sumofpoints': sumofpoints})

    # def get_queryset(self):
    #     # invoiceproductlist = InvoiceProductsList.objects.filter(invoice=self.kwargs.get('invoice_id'))
    #     return invoiceproductlist
