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
from django.urls import path
from Loyalty_program_app.views import Base, ProductAddView, UserMainSite, ProductUpdateView, InvoiceListView
from Loyalty_program_app.views import InvoiceDetaliView, InvoiceAddView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', Base.as_view(), name='base'),
    path('user-main-site/', UserMainSite.as_view(), name='user-main-site'),
    path('product-add/', ProductAddView.as_view(), name='product-add'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('invoices-list/', InvoiceListView.as_view(), name='invoices-list'),
    path('invoice-detail/<int:pk>/', InvoiceDetaliView.as_view(), name='invoice-detail'),
    path('invoice-add/', InvoiceAddView.as_view(), name='invoice-add')
]
