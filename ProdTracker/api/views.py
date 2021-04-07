from django.shortcuts import render
from rest_framework import viewsets
from product.models import Branch,Vendor,Product,Transfer
from .serializers import BranchSerializer,VendorSerializer,ProductSerializer,TrasferSerializer

# Create your views here.


class BranchViewSet(viewsets.ModelViewSet):
    serializer_class=BranchSerializer
    queryset = Branch.objects.all().order_by('-id')


class VendorViewSet(viewsets.ModelViewSet):
    serializer_class=VendorSerializer
    queryset = Vendor.objects.all().order_by('-id')

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset = Product.objects.all().order_by('-id')


class TransferViewSet(viewsets.ModelViewSet):
    serializer_class=TrasferSerializer
    queryset = Transfer.objects.all().order_by('-id')