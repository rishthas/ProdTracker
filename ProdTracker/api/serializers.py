from rest_framework import serializers
from product.models import Branch,Vendor,Product,Transfer

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Branch
        fields="__all__"

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields="__all__"