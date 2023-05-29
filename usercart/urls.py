from django.urls import path
from .views import CartDetailsAPIView

urlpatterns = [
    path('details', CartDetailsAPIView.as_view(), name='user-cart'),
    path('details/<int:product_id>', CartDetailsAPIView.as_view(), name='user-cart-delete'),
]