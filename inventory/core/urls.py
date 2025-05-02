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

urlpatterns = [
    path('',include(router.urls)),
    path('api/register/',RegisterView.as_view(),name='register'),
    path('api/login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
