from django.urls import path
from .views import CategoryList, CategoryDetail, ProductList, ProductDetail, ProductListByCategoryName

urlpatterns = [
    path('categories', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>', CategoryDetail.as_view(), name='category-detail'),
    path('', ProductList.as_view(), name='product-list'),
    path('<int:pk>', ProductDetail.as_view(), name='product-detail'),
    path('by_category_name/<str:category_name>', ProductListByCategoryName.as_view(), name='product-list-by-category'),
]
