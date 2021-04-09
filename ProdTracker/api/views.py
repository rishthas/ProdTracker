from django.shortcuts import render
from rest_framework import viewsets
from product.models import Branch,Vendor,Product,Transfer
from .serializers import BranchSerializer,VendorSerializer,ProductSerializer,TrasferSerializer,ProductAggSerializer
from django.db.models import Count
import datetime
from rest_framework.decorators import action
from rest_framework.response import Response




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

    def get_queryset(self):
        queryset = Product.objects.all()

        if self.request.query_params.get('for_transfer', None) == "Y":
            print("for_transfer")
            queryset = queryset.filter(invoce_no__isnull=True)
        if self.request.query_params.get('for_invoice', None) == "Y":
            print("for_transfer")
            queryset = queryset.filter(invoce_no__isnull=True,branch__isnull=False)
        
        if self.request.query_params.get('to_branch', None):
            print("to_branch")
            queryset = queryset.exclude(branch__id=self.request.query_params.get('to_branch', None))
        
        if self.request.query_params.get('p_from_date', None):
            print("p_from_date")
            queryset = queryset.filter(purchase_date__gte=datetime.datetime.strptime(self.request.query_params.get('p_from_date', None),'%d-%m-%Y').date())
        if self.request.query_params.get('p_to_date', None):
            print("p_to_date")
            queryset = queryset.filter(purchase_date__lte=datetime.datetime.strptime(self.request.query_params.get('p_to_date', None),'%d-%m-%Y').date())
        if self.request.query_params.get('i_from_date', None):
            print("i_from_date")
            queryset = queryset.filter(invoice_date__gte=datetime.datetime.strptime(self.request.query_params.get('i_from_date', None),'%d-%m-%Y').date())
        if self.request.query_params.get('i_to_date', None):
            print("i_to_date")
            queryset = queryset.filter(invoice_date__lte=datetime.datetime.strptime(self.request.query_params.get('i_to_date', None),'%d-%m-%Y').date())
        
        if self.request.query_params.get('branch', None):
            print("branch")
            queryset = queryset.filter(branch__id=self.request.query_params.get('branch', None))
        if self.request.query_params.get('vendor', None):
            print("vendor")
            queryset = queryset.filter(vendor__id=self.request.query_params.get('vendor', None))
        if self.request.query_params.get('model', None):
            print("model")
            queryset = queryset.filter(model_no=self.request.query_params.get('model', None))
        if self.request.query_params.get('serial_num', None):
            print("serial_num")
            queryset = queryset.filter(serial_num=self.request.query_params.get('serial_num', None))
        if self.request.query_params.get('invoice_no', None):
            print("invoice_no")
            queryset = queryset.filter(invoce_no=self.request.query_params.get('invoice_no', None))

        if self.request.query_params.get('cust_code', None):
            print("cust_code")
            queryset = queryset.filter(customer_code=self.request.query_params.get('cust_code', None))


        queryset = queryset.order_by('-id')
        return queryset
    

    @action(detail=False, methods=['POST'])
    def transfer(self, request):
        response = {}
        transfer_date = datetime.datetime.strptime(request.POST["transfer_date"],'%d-%m-%Y').date()
        print(transfer_date)
        to_branch = Branch.objects.get(id=request.POST["to_branch"])
        print(to_branch)
        products = request.POST.getlist('products[]')
        print(products)
        for product_id in products:
            product = Product.objects.get(id=product_id)
            if product.branch:
                transfer = Transfer(product=product,branch=product.branch,date=transfer_date,status="O",remark="Manual Transfer")
                transfer.save()
            transfer = Transfer(product=product,branch=to_branch,date=transfer_date,status="I",remark="Manual Transfer")
            transfer.save()
            product.branch = to_branch
            product.save()
        response["message"] = "Transfered"
        return Response(response)

        
    @action(detail=False, methods=['POST'])
    def link_invoice(self, request):
        response = {}
        invoice_date = datetime.datetime.strptime(request.POST["invoice_date"],'%d-%m-%Y').date()
        print(invoice_date)
        invoice_no = request.POST["invoice_no"]
        print(invoice_no)
        cust_code = request.POST["cust_code"]
        print(cust_code)
        products = request.POST.getlist('products[]')
        print(products)
        for product_id in products:
            product = Product.objects.get(id=product_id)
            
            transfer = Transfer(product=product,branch=product.branch,date=invoice_date,status="0",remark="{}/{}".format(invoice_no,cust_code))
            transfer.save()
            product.invoice_date = invoice_date
            product.invoce_no = invoice_no
            product.customer_code = cust_code

            product.save()
        response["message"] = "Linked"
        return Response(response)






class ProductAggViewSet(viewsets.ModelViewSet):
    serializer_class=ProductAggSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        if self.request.query_params.get('uninvoiced', None):
            return Product.objects.filter(invoce_no__isnull=True).values('vendor','model_no').annotate(cnt=Count('id')).values('vendor__name','vendor__code','model_no','cnt')
        
        if self.request.query_params.get('untransfered', None):
            return Product.objects.filter(branch__isnull=True).values('vendor','model_no').annotate(cnt=Count('id')).values('vendor__name','vendor__code','model_no','cnt')

        return Product.objects.values('vendor','model_no').annotate(cnt=Count('id')).values('vendor__name','vendor__code','model_no','cnt')


class TransferViewSet(viewsets.ModelViewSet):
    serializer_class=TrasferSerializer
    queryset = Transfer.objects.all().order_by('-event_time')

