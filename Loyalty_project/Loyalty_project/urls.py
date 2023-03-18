"""Loyalty_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Loyalty_program_app.views import MainSite, SignUpView, ProductAddView, UserMainSite, ProductUpdateView, InvoiceListView
from Loyalty_program_app.views import InvoiceDetaliView, InvoiceAddView, PurchesSummary, PrizesAddView, PrizeOrder
from Loyalty_program_app.views import PrizeDetail, OrderHistory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("signup/", SignUpView.as_view(), name ="signup"),
    path('main/', MainSite.as_view(), name='main-site'),
    path('user-main-site/', UserMainSite.as_view(), name='user-main-site'),
    path('product-add/', ProductAddView.as_view(), name='product-add'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('invoices-list/', InvoiceListView.as_view(), name='invoices-list'),
    path('invoice-detail/<int:pk>/', InvoiceDetaliView.as_view(), name='invoice-detail'),
    path('invoice-add/', InvoiceAddView.as_view(), name='invoice-add'),
    path('purchase-summary/<int:year>', PurchesSummary.as_view(), name='pruchase-summary'),
    path('prizes-add/', PrizesAddView.as_view(), name='prizes-add'),
    path('prizes-order/', PrizeOrder.as_view(), name='prizes-order'),
    path('prize-detail/<int:pk>/', PrizeDetail.as_view(), name='prize-detail'),
    path('orders-history/', OrderHistory.as_view(), name='orders-history'),
]
