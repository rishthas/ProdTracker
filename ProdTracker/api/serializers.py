from rest_framework import serializers
from product.models import Branch,Vendor,Product,Transfer

class BranchSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model=Branch
        fields="__all__"

class VendorSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model=Vendor
        fields="__all__"


class ProductSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model=Product
        fields="__all__"
    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        representation['branch'] = BranchSerializer(instance.branch).data
        representation['vendor'] = VendorSerializer(instance.vendor).data
        return representation 

class TrasferSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model=Transfer
        fields="__all__"
    
    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        representation['branch'] = BranchSerializer(instance.branch).data
        representation['product'] = ProductSerializer(instance.product).data
        return representation 