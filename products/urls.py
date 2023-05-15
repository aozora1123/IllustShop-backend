from django.urls import path
from .views import CategoryList, CategoryDetail, ProductList, ProductDetail, ProductListByCategoryName

urlpatterns = [
    path('categories', CategoryList.as_view()),
    path('categories/<int:pk>', CategoryDetail.as_view()),
    path('', ProductList.as_view()),
    path('<int:pk>', ProductDetail.as_view()),
    path('by_category_name/<str:category_name>', ProductListByCategoryName.as_view()),
]
