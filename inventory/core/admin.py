from django.contrib import admin
from .models import Customer,Item,Category,Supplier

admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Supplier)

# Register your models here.
