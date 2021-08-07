from rest_framework import serializers
from product.models import Branch,Vendor,Product,Transfer,StockCheck,Model
import calendar
from django.contrib.auth.models import User
from accounts.models import Role,Profile


class RoleSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model = Role
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"
    def to_representation(self,instance):
        representation =  super(ProfileSerializer,self).to_representation(instance)
        representation['role_id'] = RoleSerializer(instance.role_id).data
        return representation 
class UserSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model = User
        fields = ('id','Action','username', 'first_name','last_name','email','profile')

    def to_representation(self,instance):
        representation =  super(UserSerializer,self).to_representation(instance)
        representation['profile'] = ProfileSerializer(instance.profile).data
        return representation 


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

class ModelSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model=Model
        fields="__all__"

    def to_representation(self,instance):
        representation =  super(ModelSerializer,self).to_representation(instance)
        representation['vendor'] = VendorSerializer(instance.vendor).data
        return representation 


class ProductSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    class Meta:
        model=Product
        fields="__all__"
    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        representation['branch'] = BranchSerializer(instance.branch).data
        representation['model'] = ModelSerializer(instance.model).data
        return representation 


class ProductAggSerializer(serializers.ModelSerializer):
    cnt = serializers.IntegerField()
    # vendor = VendorSerializer()
    # vendor_name = serializers.CharField(source="vendor__name",read_only=True)
    # vendor_code = serializers.CharField(source="vendor__code",read_only=True)
    vendor_name = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()
    model_no = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('vendor_name','vendor_code','model_no', 'cnt')
    def get_vendor_name(self,obj):
        print(obj)
        return obj['model__vendor__name']

    def get_vendor_code(self,obj):
        print(obj)
        return obj['model__vendor__code']

    def get_model_no(self,obj):
        print(obj)
        return obj['model__name']
        
class StockSummarySerializer(serializers.ModelSerializer):
    available = serializers.IntegerField()
    stocked = serializers.IntegerField()
    vendor_name = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()
    model_no = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('vendor_name','vendor_code','model_no', 'branch_name','available','stocked')
    def get_vendor_name(self,obj):
        # print(obj)
        return obj['model__vendor__name']

    def get_vendor_code(self,obj):
        # print(obj)
        return obj['model__vendor__code']

    def get_model_no(self,obj):
        # print(obj)
        return obj['model__name']
    def get_branch_name(self,obj):
        return obj['branch__name']
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



class StockCheckSerializer(serializers.ModelSerializer):
    Action = serializers.CharField(max_length=50,default=None,read_only=True)
    month_str = serializers.SerializerMethodField()
    class Meta:
        model=StockCheck
        fields="__all__"
    
    def to_representation(self, instance):
        representation = super(StockCheckSerializer, self).to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        return representation
    
    def get_month_str(self,obj):
        return calendar.month_name[int(obj.month)]

