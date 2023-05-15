#from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return super().get_permissions()

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductListByCategoryName(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        try:
            category = Category.objects.get(name=self.kwargs['category_name'])
        except Category.DoesNotExist:
            raise
        queryset = category.products.all() # 利用category的related_name，反向查詢所對應的資料
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            # get_queryset只能回傳queryset object
            # 透過override list function處理查詢之category_name不存在的情形，以區別category_name存在，但對應products數量為0的情形
            queryset = self.get_queryset()
        except Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
