from django.contrib import admin
from core.models import Product, Material, Warehouse, ProductMaterial

admin.site.register(Warehouse)
admin.site.register(Material)
admin.site.register(Product)
admin.site.register(ProductMaterial)
