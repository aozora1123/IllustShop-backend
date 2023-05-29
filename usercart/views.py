from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Cart, Product
from .serializers import CartSerializer


class CartDetailsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'message': '', 'exist': 'False', 'products': []}, status=status.HTTP_404_NOT_FOUND)
        productsList = list(cart.products.all().values()) # 將QuerySet轉換為Dict後，再轉為list
        return Response({'message': '', 'exist': 'True', 'products': productsList}, status=status.HTTP_200_OK)

    def post(self, request): 
        if not request.data.get('product_id'):
            return Response({'message': 'Error, product_id parameter is required', 'exist': 'False'}, status=status.HTTP_400_BAD_REQUEST)
        # 先檢查user是否已經有cart，若沒有則建立一個新的
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        # 加入選取的商品進入cart
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Error, product not found', 'exist': 'False'}, status=status.HTTP_404_NOT_FOUND)
        if cart.products.filter(id=product_id).exists():
            return Response({'message': 'product exist', 'exist': 'True'}, status=status.HTTP_200_OK)
        cart.products.add(product)
        cart.save()
        return Response({'message': 'success', 'exist': 'False'}, status=status.HTTP_200_OK)

    def delete(self, request, product_id=None):
        if product_id == None:
            return Response({'message': 'product_id is required', 'status': status.HTTP_400_BAD_REQUEST})
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        try:
            product_instance = Product.objects.get(id=product_id)
            cart.products.remove(product_instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'status': status.HTTP_400_BAD_REQUEST})

            