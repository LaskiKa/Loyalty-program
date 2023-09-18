from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from Loyalty_program_app.models import Products, InvoiceProductsList, UserProfile, Invoices, Prizes, Carts, CartItems
from django.db.models.functions import ExtractYear
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.list import ListView
from datetime import date


# Create your views here.
class MainSite(View):
    """Main site of LP app"""
    def get(self, request):
        return render(request,
                      'Loyalty_program_app/base.html')

class ProductList(View):
    """View with premium products"""
    def get(self, request):
        products = Products.objects.all()
        return render(request,
                      'Loyalty_program_app/products_list.html',
                      {'products': products})


class SignUpView(CreateView):
    """Sign up View"""
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserMainSite(LoginRequiredMixin, View):
    """Main site of LP app for logged users"""
    def get(self, request):
        userpoints = UserProfile.objects.get(user=self.request.user).points
        return render(request,
                      "Loyalty_program_app/user-main-site.html",
                      context={'userpoints': userpoints})


class ProductAddView(LoginRequiredMixin, CreateView):
    """"""
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

    def get(self, request, year=0):
        userpoints = UserProfile.objects.get(user=self.request.user).points
        invoices = Invoices.objects.filter(
            user=self.request.user.id).order_by('-sale_date')
        products = Products.objects.all()
        productsummary = {}
        years = []

        for invoice in invoices:
            years.append(invoice.sale_date.year)
        years = list(dict.fromkeys(years))

        if year == 0:
            userinvoices = Invoices.objects.filter(user=self.request.user.id)

        else:
            userinvoices = Invoices.objects.filter(
                user=self.request.user.id).filter(
                sale_date__year=year).order_by('-sale_date')

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

        return render(request,
                      'Loyalty_program_app/purchase_summary.html',
                      context={"userpoints": userpoints,
                               "productsummary": productsummary.items(),
                               'years': years})


class PrizesAddView(CreateView):
    model = Prizes
    fields = '__all__'
    success_url = '/base/'

class PrizesList(View):
    def get(self, request):
        prizes = Prizes.objects.all()
        return render(request,
                      "Loyalty_program_app/prize_list.html",
                      {"prizes": prizes})


class PrizeOrder(LoginRequiredMixin, View):

    def get(self, request):
        userpoints = UserProfile.objects.get(user=self.request.user).points
        prizes = Prizes.objects.filter(is_active=True)

        return render(request,
                      'Loyalty_program_app/prize_order.html',
                      context={
                          "prizes": prizes,
                          "userpoints": userpoints,
                      })


class PrizeDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        userpoints = UserProfile.objects.get(user=self.request.user).points
        prize = Prizes.objects.get(pk=pk)
        return render(request,
                      'Loyalty_program_app/prize_detail.html',
                      context={
                          "prize": prize,
                          "userpoints": userpoints
                      })

    def post(self, reqest, pk):
        "Wybór ilości nagród do zamówienia"

        """DO poprawy - przyjrzeć się modelom !!!"""
        userpoints = UserProfile.objects.get(user=self.request.user).points
        prize = Prizes.objects.get(pk=pk)

        if reqest.POST['order'] == 'Zamów nagrodę':
            quantity = reqest.POST['quantity']
            costsum = int(quantity) * prize.points_value
            return render(reqest,
                          'Loyalty_program_app/order.html',
                          context={
                              "prize": prize,
                              "userpoints": userpoints,
                              "quantity": quantity,
                              "costsum": costsum
                          })

        elif reqest.POST['order'] == 'Potwierdzam i zamawiam':
            """Stworzenie klientowi koszyka z nagrodą, obciążenia salad punktowego kwotą nagrody,
                zmniejszenie ilości dostępnej nagrody"""

            quantity = reqest.POST['quantity']

            cart = Carts.objects.create(user=UserProfile.objects.get(user=self.request.user),
                                        order_date=date.today())

            cartitem = CartItems.objects.create(cart=cart,
                                                prize=prize,
                                                quantity=quantity)

            user = UserProfile.objects.get(user=self.request.user)
            user.points -= int(quantity) * prize.points_value
            user.save()
            prize.available_quantity - int(quantity)
            prize.save()

            return HttpResponse("Dziękujemy za zakup nagrody")


class OrderHistory(LoginRequiredMixin, View):

    def get(self, request):
        user = UserProfile.objects.get(user=self.request.user)
        userpoints = UserProfile.objects.get(user=self.request.user).points
        usercartiems = CartItems.objects.filter(cart__user=user)
        spentpointssum = 0
        ordervalue = {}

        for item in usercartiems:
            prizepoints = 0
            qty = item.quantity
            points_value = item.prize.points_value
            prizepoints += int(qty * points_value)
            spentpointssum += int(qty * points_value)
            ordervalue[item.id] = prizepoints

        return render(request,
                      "Loyalty_program_app/orders-history.html",
                      context={
                          "userpoints": userpoints,
                          "usercartiems": usercartiems,
                          "ordervalue": ordervalue.items(),
                          "spentpointssum": spentpointssum
                      })
