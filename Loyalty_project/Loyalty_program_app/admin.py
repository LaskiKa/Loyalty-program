from django.contrib import admin
from Loyalty_program_app.models import UserProfile, Products, Prizes

admin.site.register(Products)
admin.site.register(UserProfile)
admin.site.register(Prizes)

# Register your models here.
