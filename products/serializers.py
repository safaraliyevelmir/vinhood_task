from typing import Union
from .models import Product,ProductCategory, WishlistItem
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['pk','name']


class ProductSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = ['pk','name','user','price','category','created_time']
    
        read_only_fields = ('created_time',)

        extra_kwargs = {
            'updated_time':{'write_only': True},
        }




class WishlistItemSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs) :
        super().__init__(many=True, *args, **kwargs)


    class Meta:
        model = WishlistItem
        fields = ['user', 'product']




