from django.shortcuts import render
from rest_framework import viewsets, status
from product.models import Branch, Vendor, Product, Transfer, StockCheck,Model
from .serializers import BranchSerializer, VendorSerializer, ProductSerializer, TrasferSerializer, ProductAggSerializer
from .serializers import StockCheckSerializer, UserSerializer,RoleSerializer,ProfileSerializer,ModelSerializer
from django.db.models import Count,Q
import datetime
import calendar
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from accounts.models import Role,Profile,RoleAccess
import json
from django.conf import settings




# Create your views here.

class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def handleParent(self,menu_tree,role):
        print("In handleParent")
        for menu in menu_tree:
            print(menu)
            if 'submenu' in menu:
                print("Has Submenu")
                for submenu in menu["submenu"]:
                    if 'submenu' in submenu:
                        self.handleParent(submenu, role)
                    else:
                        if RoleAccess.objects.filter(role=role,access_point=submenu["ref"]):
                            print("Submenu has acccess, so adding to parent with child")
                            access, created = RoleAccess.objects.get_or_create(role=role,access_point=menu["ref"],access_string="child")
                            access.save()
    
    @action(detail=False, methods=['POST'])
    def add_with_access(self, request):
        print(request.POST)
        role_id = request.POST['role_id']
        role_desc = request.POST['role_desc']
        if Role.objects.filter(role_id=role_id):
            return Response({"message":"Role Id already exists"},status=status.HTTP_400_BAD_REQUEST)

        role = Role(role_id=role_id,description=role_desc)
        role.save()

        print(request.POST.getlist('access_matrix[]'))
        for  access_item in request.POST.getlist('access_matrix[]'):
            access_item_json = json.loads(access_item)
            print(access_item_json['access_ref'])
            role_access = RoleAccess(role=role,access_point=access_item_json['access_ref'],access_string=access_item_json['access_type'])
            role_access.save()
        self.handleParent(setting.ADMIN_MENU,role)
        return Response({"message":"The Role {}is Created".format(role_id)})
    
    
    @action(detail=False, methods=['POST'])
    def editrole(self, request):
        print(request.POST)
        role_id = request.POST['role_id']
        role_desc = request.POST['role_desc']
        if not Role.objects.filter(role_id=role_id):
            return Response({"message":"Role Id doesnot exist"},status=status.HTTP_400_BAD_REQUEST)

        role = Role.objects.get(role_id=role_id)
        role.description = role_desc
        role.save()

        RoleAccess.objects.filter(role=role).delete()

        print(request.POST.getlist('access_matrix[]'))
        for  access_item in request.POST.getlist('access_matrix[]'):
            access_item_json = json.loads(access_item)
            print(access_item_json['access_ref'])
            role_access = RoleAccess(role=role,access_point=access_item_json['access_ref'],access_string=access_item_json['access_type'])
            role_access.save()
        self.handleParent(settings.ADMIN_MENU,role)
        return Response({"message":"The Role {}is Edited".format(role_id)})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all().order_by('-id')


class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all().order_by('-id')

class ModelViewSet(viewsets.ModelViewSet):
    serializer_class = ModelSerializer
    queryset = Model.objects.all().order_by('-id')


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')

    def get_queryset(self):
        queryset = Product.objects.all()

        if self.request.query_params.get('for_transfer', None) == "Y":
            print("for_transfer")
            queryset = queryset.filter(invoce_no__isnull=True)
        if self.request.query_params.get('for_invoice', None) == "Y":
            print("for_transfer")
            queryset = queryset.filter(
                invoce_no__isnull=True, branch__isnull=False)

        
        if self.request.query_params.get('for_cr_note', None) == "Y":
            print("for_cr_note")
            queryset = queryset.filter(
                invoce_no__isnull=False, branch__isnull=False)

        if self.request.query_params.get('to_branch', None):
            print("to_branch")
            queryset = queryset.exclude(
                branch__id=self.request.query_params.get('to_branch', None))

        if self.request.query_params.get('p_from_date', None):
            print("p_from_date")
            queryset = queryset.filter(purchase_date__gte=datetime.datetime.strptime(
                self.request.query_params.get('p_from_date', None), '%d-%m-%Y').date())
        if self.request.query_params.get('p_to_date', None):
            print("p_to_date")
            queryset = queryset.filter(purchase_date__lte=datetime.datetime.strptime(
                self.request.query_params.get('p_to_date', None), '%d-%m-%Y').date())
        if self.request.query_params.get('i_from_date', None):
            print("i_from_date")
            queryset = queryset.filter(invoice_date__gte=datetime.datetime.strptime(
                self.request.query_params.get('i_from_date', None), '%d-%m-%Y').date())
        if self.request.query_params.get('i_to_date', None):
            print("i_to_date")
            queryset = queryset.filter(invoice_date__lte=datetime.datetime.strptime(
                self.request.query_params.get('i_to_date', None), '%d-%m-%Y').date())

        if self.request.query_params.get('branch', None):
            print("branch")
            queryset = queryset.filter(
                branch__id=self.request.query_params.get('branch', None))
        if self.request.query_params.get('vendor', None):
            print("vendor")
            queryset = queryset.filter(
                model__vendor__id=self.request.query_params.get('vendor', None))
        if self.request.query_params.get('model', None):
            print("model")
            queryset = queryset.filter(
                model__id=self.request.query_params.get('model', None))

        if self.request.query_params.get('pur_invoce_no', None):
            print("pur_invoce_no")
            queryset = queryset.filter(
                pur_invoce_no__icontains=self.request.query_params.get('pur_invoce_no', None))
        if self.request.query_params.get('serial_num', None):
            print("serial_num")
            queryset = queryset.filter(
                serial_num=self.request.query_params.get('serial_num', None))
        if self.request.query_params.get('invoice_no', None):
            print("invoice_no")
            queryset = queryset.filter(
                invoce_no=self.request.query_params.get('invoice_no', None))

        if self.request.query_params.get('cust_code', None):
            print("cust_code")
            queryset = queryset.filter(
                customer_code=self.request.query_params.get('cust_code', None))

        if self.request.query_params.get('stock_rpt', None) == "Y":
            queryset = queryset.filter(invoce_no__isnull=True)
            if self.request.query_params.get('month', None) and self.request.query_params.get('year', None):
                print("In Month")
                ref_date = datetime.date(int(self.request.query_params.get('year')), int(self.request.query_params.get('month'))+1, 1)
                print(ref_date)
                queryset = queryset.filter(purchase_date__lt=ref_date)

                if self.request.query_params.get('stock', None) == "Y":
                    queryset = queryset.filter(id__in=StockCheck.objects.filter(month=self.request.query_params.get(
                        'month', None), year=self.request.query_params.get('year', None)).values_list('product__id', flat=True))
                else:
                    queryset = queryset.exclude(id__in=StockCheck.objects.filter(month=self.request.query_params.get(
                        'month', None), year=self.request.query_params.get('year', None)).values_list('product__id', flat=True))
            else:
                print("In else")
                if self.request.query_params.get('stock', None) == "Y":
                    print("In else ---- > Y")
                    queryset = queryset.filter(id__in=StockCheck.objects.values_list('product__id', flat=True))
                else:
                    queryset = queryset.exclude(id__in=StockCheck.objects.values_list('product__id', flat=True))
            print(queryset.query)

        queryset = queryset.order_by('-id')
        return queryset
    @action(detail=False, methods=['GET'])
    def customers(self,request):
        response = []
        print(request.query_params)
        response = Product.objects.filter(customer_code__isnull=False,customer_code__icontains=request.query_params.get('q')).values_list('customer_code',flat=True).distinct()
        return Response(response)
    @action(detail=False, methods=['POST'])
    def transfer(self, request):
        response = {}
        transfer_date = datetime.datetime.strptime(
            request.POST["transfer_date"], '%d-%m-%Y').date()
        print(transfer_date)
        to_branch = Branch.objects.get(id=request.POST["to_branch"])
        print(to_branch)
        products = request.POST.getlist('products[]')
        print(products)
        for product_id in products:
            product = Product.objects.get(id=product_id)
            if product.branch:
                transfer = Transfer(product=product, branch=product.branch,
                                    date=transfer_date, status="O", remark="Manual Transfer")
                transfer.save()
            transfer = Transfer(product=product, branch=to_branch,
                                date=transfer_date, status="I", remark="Manual Transfer")
            transfer.save()
            product.branch = to_branch
            product.save()
        response["message"] = "Transfered"
        return Response(response)
    
    @action(detail=False, methods=['POST'])
    def credit_note(self,request):
        print("Credit Note")
        response = {}
        products = request.POST.getlist('products[]')
        for product_id in products:
            product = Product.objects.get(id=product_id)
            product.invoce_no = None
            product.invoice_date = None
            product.customer_code = None
            product.save()
        response["message"] = "Marked"
        return Response(response)

    @action(detail=False, methods=['POST'])
    def link_invoice(self, request):
        response = {}
        invoice_date = datetime.datetime.strptime(
            request.POST["invoice_date"], '%d-%m-%Y').date()
        print(invoice_date)
        invoice_no = request.POST["invoice_no"]
        print(invoice_no)
        cust_code = request.POST["cust_code"]
        print(cust_code)
        products = request.POST.getlist('products[]')
        print(products)
        for product_id in products:
            product = Product.objects.get(id=product_id)

            transfer = Transfer(product=product, branch=product.branch, date=invoice_date,
                                status="O", remark="{}/{}".format(invoice_no, cust_code))
            transfer.save()
            product.invoice_date = invoice_date
            product.invoce_no = invoice_no
            product.customer_code = cust_code

            product.save()
        response["message"] = "Linked"
        return Response(response)

    @action(detail=False, methods=['POST'])
    def do_stock(self, request):
        response = {}
        serial_num = request.POST["serial_num"]
        model = request.POST["model"]
        month = request.POST["month"]
        year = request.POST["year"]

        queryset = Product.objects.filter(serial_num=serial_num)
        if not queryset:
            return Response({"message": "The Product is not available"}, status=status.HTTP_400_BAD_REQUEST)
        if model.strip():
            queryset = queryset.filter(model__id=model)
        

        count = queryset.count()
        if count > 1:
            return Response({"message": "There are multiple Product with the same serial number [{}], please select the Vendor or Model and scan again".format(serial_num)}, status=status.HTTP_400_BAD_REQUEST)

        queryset = queryset.filter(invoce_no__isnull=True)
        print(queryset.query)
        if not queryset:
            return Response({"message": "The Product is already Invoiced in the system"}, status=status.HTTP_400_BAD_REQUEST)

        product = queryset.first()
        print(product)
        if StockCheck.objects.filter(product=product, month=month, year=year):
            return Response({"message": "The Product is already marked for stock for the month/year [{}/{}]".format(calendar.month_name[int(month)], year)}, status=status.HTTP_400_BAD_REQUEST)

        stock = StockCheck(product=product, month=month, year=year)
        stock.save()

        return Response(response)

    @action(detail=False, methods=['GET'])
    def stocks(self, request):
        queryset = Product.objects.all()
        queryset = queryset.filter(invoce_no__isnull=True)
        if self.request.query_params.get('vendor', None):
            print("vendor")
            queryset = queryset.filter(
                vendor__id=self.request.query_params.get('vendor', None))
        if self.request.query_params.get('model', None):
            print("model")
            queryset = queryset.filter(
                model_no=self.request.query_params.get('model', None))
        if self.request.query_params.get('month', None) and self.request.query_params.get('year', None):
            print("In Month")
            ref_date = datetime.date(int(self.request.query_params.get('year')), int(self.request.query_params.get('month'))+1, 1)
            print(ref_date)
            if self.request.query_params.get('stock', None) == "Y":
                queryset = queryset.filter(id__in=StockCheck.objects.filter(month=self.request.query_params.get(
                    'month', None), year=self.request.query_params.get('year', None)).values_list('product__id', flat=True))
            else:
                queryset = queryset.exclude(id__in=StockCheck.objects.filter(month=self.request.query_params.get(
                    'month', None), year=self.request.query_params.get('year', None)).values_list('product__id', flat=True))
        else:
            print("In else")
            if self.request.query_params.get('stock', None) == "Y":
                print("In else ---- > Y")
                queryset = queryset.filter(id__in=StockCheck.objects.values_list('product__id', flat=True))
            else:
                queryset = queryset.exclude(id__in=StockCheck.objects.values_list('product__id', flat=True))
        print(queryset.query)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductAggViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAggSerializer
    queryset = Product.objects.all()
    paginator = None

    def get_queryset(self):
        if self.request.query_params.get('uninvoiced', None):
            return Product.objects.filter(invoce_no__isnull=True).values('model').annotate(cnt=Count('id')).values('model__vendor__name', 'model__vendor__code', 'model__name', 'cnt')

        if self.request.query_params.get('untransfered', None):
            return Product.objects.filter(branch__isnull=True).values('model').annotate(cnt=Count('id')).values('model__vendor__name', 'model__vendor__code', 'model__name', 'cnt')
        
        if self.request.query_params.get('unstocked', None):
            if self.request.query_params.get('lastmonth', None):
                first_day_of_this_month = datetime.date.today().replace(day=1)

                return Product.objects.filter(invoce_no__isnull=True,purchase_date__lt=first_day_of_this_month).values('model').exclude(id__in=StockCheck.objects.filter(Q(month__lt=first_day_of_this_month.month,year=first_day_of_this_month.year)|Q(year__lt=first_day_of_this_month.year)).values_list('product__id', flat=True)).annotate(cnt=Count('id')).values('model__vendor__name', 'model__vendor__code', 'model__name', 'cnt')
            if self.request.query_params.get('thismonth', None):
                first_day_of_this_month = datetime.date.today().replace(day=1)
                return Product.objects.filter(invoce_no__isnull=True,purchase_date__gte=first_day_of_this_month).values('model').exclude(id__in=StockCheck.objects.filter(month__gte=first_day_of_this_month.month,year=first_day_of_this_month.year).values_list('product__id', flat=True)).annotate(cnt=Count('id')).values('model__vendor__name', 'model__vendor__code', 'model__name', 'cnt')
        return Product.objects.values('model').annotate(cnt=Count('id')).values('model__vendor__name', 'model__vendor__code', 'model__name', 'cnt')


class TransferViewSet(viewsets.ModelViewSet):
    serializer_class = TrasferSerializer
    queryset = Transfer.objects.all().order_by('-event_time')


class StockCheckViewSet(viewsets.ModelViewSet):
    serializer_class = StockCheckSerializer
    queryset = StockCheck.objects.all().order_by('-event_time')

    def get_queryset(self):
        queryset = StockCheck.objects.all()

        if self.request.query_params.get('month', None) and self.request.query_params.get('year', None):
            queryset = queryset.filter(month=self.request.query_params.get(
                'month', None), year=self.request.query_params.get('year', None))
        queryset = queryset.order_by('-event_time')
        return queryset
