from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer,Item,Category,StockEntry,StockExit,Supplier
from .serializers import ItemSerializer,CategorySerializer,CustomerSerializer,StockEntrySerializer,StockExitSerializer,SupplierSerializer
from django.db.models import Sum,Min,Max


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

class StockEntryViewSet(viewsets.ModelViewSet):
    queryset = StockEntry.objects.all()
    serializer_class=StockEntrySerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return StockEntry.objects.filter(added_by=self.request.user)

    def perform_create(self, serializer):
         serializer.save(added_by=self.request.user)

class StockExitViewSet(viewsets.ModelViewSet):
    queryset=StockExit.objects.all()
    serializer_class=StockExitSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return  StockExit.objects.filter(removed_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(removed_by=self.request.user)    

# Building a Dashboard View

class DashBoardView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        total_items=Item.objects.count()
        total_categories=Category.objects.count()
        total_entries=StockEntry.objects.count()
        total_exists=StockExit.objects.count()

        total_stock_quantity=Item.objects.aggregate(quantity_sum=Sum("quantity"))['quantity_sum'] or 0

        low_stock_items = Item.objects.filter(quantity__lt=10).values('item_name', 'quantity')

        most_stocked=Item.objects.order_by('-quantity').first()
        least_stocked=Item.objects.order_by('quantity').first()

        data={
            'total_items':total_items,
            'total_categories':total_categories,
            'total_entries':total_entries,
            'total_exists':total_exists,
            'total_stock_quantity':total_stock_quantity,
            'low_stock_items': list(low_stock_items),
            'most_stocked_item': {
                'name': most_stocked.item_name if most_stocked else None,
                'quantity': most_stocked.quantity if most_stocked else None
            },
            'least_stocked_item': {
                'name': least_stocked.item_name if least_stocked else None,
                'quantity': least_stocked.quantity if least_stocked else None
            }
        }

        return Response(data)
