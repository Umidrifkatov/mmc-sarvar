from django.urls import path
from .views import HomeView, CatalogListView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
] 