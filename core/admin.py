from django.contrib import admin
from .models import Business, Product, Product_Media, Product_review

# Register your models here.

admin.site.register(Business)
admin.site.register(Product_Media)
admin.site.register(Product)
admin.site.register(Product_review)