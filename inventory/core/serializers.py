from rest_framework import serializers
from .models import Customer,Supplier,StockExit,StockEntry,Item,Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','owner']
        

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields='__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['name','email','phone']

class ItemSerializer(serializers.ModelSerializer):
    date_added=serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    category=CategorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='category', write_only=True)

    supplier=SupplierSerializer(read_only=True)
    supplier_id=serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(),source='supplier', write_only=True)

    class Meta:
        model=Item
        fields=['item_name','category','category_id','supplier','supplier_id','description','quantity','date_added']
        

class StockEntrySerializer(serializers.ModelSerializer):
    
    date_added=serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    supplier=SupplierSerializer(read_only=True)
    supplier_id=serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(),source='supplier', write_only=True)

    item=ItemSerializer(read_only=True)
    item_id=serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(),source='item',write_only=True)

    class Meta:
        model=StockEntry
        fields=['id', 'item', 'item_id', 'quantity', 'supplier', 'supplier_id', 'date_added']

class StockExitSerializer(serializers.ModelSerializer):
    date_removed=serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), source='item', write_only=True)

    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)

    class Meta:
        model=StockExit
        fields=['id', 'item', 'item_id', 'quantity', 'customer', 'customer_id', 'date_removed']       