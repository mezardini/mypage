import django_filters
from django_filters import RangeFilter, FilterSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Product


# class ProductFilter(django_filters.FilterSet):
#     price = RangeFilter()
#     Product_type = {'Product_type': ['exact']}
#     contract_type = {'contract_type': ['exact']}
#     class Meta:
#         model = Product
#         fields = ['date_created',  'product_price']

class PriceFilter(FilterSet):
    price = RangeFilter()
    
    class Meta:
        model = Product
        fields = ['product_price', 'date_created']
