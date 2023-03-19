from django.contrib import admin
from Loyalty_program_app.models import Products, UserProfile, Prizes

# Register your models here.

admin.site.register(Prizes)
admin.site.register(Products)
admin.site.register(UserProfile)