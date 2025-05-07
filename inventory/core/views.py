from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly,IsAdmin,IsStaffOrAdmin,IsViewerReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Customer,Item,Category,StockEntry,StockExit,Supplier
from .serializers import ItemSerializer,CategorySerializer,CustomerSerializer,StockEntrySerializer,StockExitSerializer,SupplierSerializer
from django.db.models import Sum,Min,Max
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse


# class RegisterViewSet(viewsets.ModelViewSet):
#     queryset=User.objects.all()
#     serializer_class=RegisterSerializer
    


class CustomerViewSet(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    permission_classes=[IsAuthenticated]

    filter_backends=[DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    search_fields=['name','email','phone'] 
     

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer  
    permission_classes=[IsAuthenticated]   

    filter_backends=[DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    search_fields=['name','contact_email','phone']       

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[IsAuthenticated,IsViewerReadOnly,IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    # Owners to see their own categories
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)  

    filter_backends=[DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    search_fields=['name']      

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes=[IsAuthenticated,IsViewerReadOnly,IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    # Owners to see their own items
    # def get_queryset(self):
    #     return Item.objects.filter(owner=self.request.user) 

    filter_backends=[DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields=['category','supplier']
    search_fields=['item_name'] 
    ordering_filters=['quantity','date_added']        

# Create your views here.

class StockEntryViewSet(viewsets.ModelViewSet):
    queryset = StockEntry.objects.all()
    serializer_class=StockEntrySerializer
    permission_classes = [IsStaffOrAdmin]

    def get_queryset(self):
        return StockEntry.objects.filter(added_by=self.request.user)

    def perform_create(self, serializer):
         serializer.save(added_by=self.request.user)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'supplier', 'added_by']
    search_fields = ['item__item_name']
    ordering_fields = ['date_added', 'quantity_added']     

class StockExitViewSet(viewsets.ModelViewSet):
    queryset=StockExit.objects.all()
    serializer_class=StockExitSerializer
    permission_classes = [IsStaffOrAdmin]

    def get_queryset(self):
        return  StockExit.objects.filter(removed_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(removed_by=self.request.user)    

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'customer', 'removed_by']
    search_fields = ['item__item_name']
    ordering_fields = ['date_removed', 'quantity_removed'] 
# Building a Dashboard View

class DashBoardView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        total_items=Item.objects.count()
        total_categories=Category.objects.count()
        total_entries=StockEntry.objects.count()
        total_exists=StockExit.objects.count()

        total_stock_quantity=Item.objects.aggregate(quantity_sum=Sum("quantity"))['quantity_sum'] or 0

        low_stock_items = Item.objects.filter(quantity__lt=100).values('item_name', 'quantity')

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


# Generate a report about the stock, entries and exits
class StockPDFReportView(APIView):
    permission_classes=[IsAuthenticated,IsStaffOrAdmin]
    def get(self,request):
        entries=StockEntry.objects.all()
        exits=StockExit.objects.all()

        total_entry_quantity = entries.aggregate(Sum('quantity_added'))['quantity_added__sum'] or 0
        total_exit_quantity = exits.aggregate(Sum('quantity_removed'))['quantity_removed__sum'] or 0
        net_stock = total_entry_quantity - total_exit_quantity

        context = {
            'entries': entries,
            'exits': exits,
            'total_entry_quantity': total_entry_quantity,
            'total_exit_quantity': total_exit_quantity,
            'net_stock': net_stock,
        }

        html = render_to_string('reports/stock_report.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="stock_report.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        return response

        