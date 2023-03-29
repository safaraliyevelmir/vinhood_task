from django.shortcuts import render

from rest_framework import viewsets,filters
from .serializers import ProductSerializer, CategorySerializer, WishlistItemSerializer
from .models import Product, WishlistItem
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from rest_framework.generics import ListAPIView


class ProductViewSet(viewsets.ModelViewSet):

    """
    The viewset used to perform CRUD operations on the product model.
    Users must authenticate in order to operate.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rank', 'created_time']
    permission_classes = [IsAuthenticated]



 

    def get_queryset(self):
        
        """
        Returns a filtered queryset based on the query parameters 'price_gt' and 'price_lt'.
        """
        
        queryset = super().get_queryset()
        price_gt = self.request.query_params.get('price_gt')
        price_lt = self.request.query_params.get('price_lt')

        if price_gt:
            queryset = queryset.filter(price__gte=price_gt)
        if price_lt:
            queryset = queryset.filter(price__lte=price_lt)
        return queryset


    def get_permissions(self):

        """Returns the permission based on the type of action"""

        if self.action in ["list","retrieve"]:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        """Returns the permission based on the type of action"""

        if self.action in ["list","retrieve"]:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]
    
class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=201, headers=headers)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)


class WishlistListAPIView(ListAPIView):
    """
    API endpoint that returns a list of wishlist items for a specific user.

    Parameters:
        pk (int): User ID.

    Returns:
        A JSON response containing a list of wishlist items.
    """
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Retrieves the list of wishlist items for a specific user.

        Returns:
            QuerySet: A list of WishlistItem objects.
        """
        user_id = self.kwargs.get('pk')
        queryset = WishlistItem.objects.filter(user=user_id)
        return queryset