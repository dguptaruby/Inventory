from django.contrib import admin

from .models import Company, Manager, Product, Store

admin.site.register(Company)
admin.site.register(Manager)
admin.site.register(Product)
admin.site.register(Store)
