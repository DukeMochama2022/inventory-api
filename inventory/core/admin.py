from django.contrib import admin
from .models import Customer,Item,Category,Supplier,Profile

admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Profile)

# Register your models here.
