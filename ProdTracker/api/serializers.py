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


class ProductAggSerializer(serializers.ModelSerializer):
    cnt = serializers.IntegerField()
    # vendor = VendorSerializer()
    # vendor_name = serializers.CharField(source="vendor__name",read_only=True)
    # vendor_code = serializers.CharField(source="vendor__code",read_only=True)
    vendor_name = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('vendor_name','vendor_code','model_no', 'cnt')
    def get_vendor_name(self,obj):
        print(obj)
        return obj['vendor__name']

    def get_vendor_code(self,obj):
        print(obj)
        return obj['vendor__code']
        

class TrasferSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model=Transfer
        fields="__all__"
    
    def to_representation(self, instance):
        representation = super(TrasferSerializer, self).to_representation(instance)
        representation['branch'] = BranchSerializer(instance.branch).data
        representation['product'] = ProductSerializer(instance.product).data
        return representation 