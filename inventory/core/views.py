from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from .models import Customer,Item,Category,StockEntry,StockExit,Supplier
from .serializers import ItemSerializer,CategorySerializer,CustomerSerializer,StockEntrySerializer,StockExitSerializer,SupplierSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    permission_classes=[IsAuthenticated]
    

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer  
    permission_classes=[IsAuthenticated] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Owners to see only their suppliers
    def get_queryset(self):
        return Supplier.objects.filter(owner=self.request.user)    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[IsAuthenticated,IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    # Owners to see their own categories
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)    

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes=[IsAuthenticated,IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    # Owners to see their own items
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user)      

# Create your views here.
