from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views_auth import RegisterView,LogoutView


router=DefaultRouter()
router.register(r'items',views.ItemViewSet)
router.register(r'categories',views.CategoryViewSet)
router.register(r'customers',views.CustomerViewSet)
router.register(r'suppliers',views.SupplierViewSet)
router.register(r'stock-entry',views.StockEntryViewSet, basename='stock-entry')
router.register(r'stock-exit',views.StockExitViewSet,basename='stock-exit')

urlpatterns = [
    path('',include(router.urls)),
    path('api/dashboard/', views.DashBoardView.as_view(), name='dashboard'),
    path('api/register/',RegisterView.as_view(),name='register'),
    path('api/login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
