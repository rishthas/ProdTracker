from django.shortcuts import render,redirect
from .forms import BranchForm,VendorForm,ModelForm,ProductForm
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext as _
from .models import Branch, Vendor, Product, Transfer, StockCheck,Model
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.models import RoleAccess
from django.db.models import Count, Q
from .decorators import check_access
import xlwt
from django.http import HttpResponse
# import datetime
import calendar




# Create your views here.
@login_required
def index(request):
    first_day_of_this_month = datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    print("first_day_of_this_month")
    print(first_day_of_this_month)
    first_date_of_last_month =   (first_day_of_this_month - timedelta(days=1)).replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    print("first_date_of_last_month")
    print(first_date_of_last_month)

    this_month = datetime.today().strftime("%b-%Y")
    summary = Product.objects.aggregate(
        tot_purchase=Count('id'),
        uninvoiced=Count(
            'id',
            filter=Q(invoce_no__isnull=True)
            ),
        sale=Count(
            'id',
            filter=Q(invoce_no__isnull=False)
            ),
        lastmonth=Count(
            'id',
            filter=Q(
                invoce_no__isnull=True,
                purchase_date__lt=first_day_of_this_month)&
                ~Q(id__in=StockCheck.objects.filter(Q(month=first_date_of_last_month.month,year=first_date_of_last_month.year)).values_list('product__id', flat=True)    
            )
            ),
        thismonth=Count(
            'id',
            filter=Q(
                invoce_no__isnull=True)&
                ~Q(id__in=StockCheck.objects.filter(month__gte=first_day_of_this_month.month,year=first_day_of_this_month.year).values_list('product__id', flat=True)    

            )
            ),
        intransit=Count(
            'id',
            filter=Q(status="O")
            )
            )
    branch_wise = Product.objects.values('branch').annotate(
        tot_purchase=Count('id'),
        uninvoiced=Count(
            'id',
            filter=Q(invoce_no__isnull=True)
            ),
        sale=Count(
            'id',
            filter=Q(invoce_no__isnull=False)
            ),
        lastmonth=Count(
            'id',
            filter=Q(
                invoce_no__isnull=True,
                purchase_date__lt=first_day_of_this_month)&
                ~Q(id__in=StockCheck.objects.filter(Q(month=first_date_of_last_month.month,year=first_date_of_last_month.year)).values_list('product__id', flat=True)    
            )
            ),
        thismonth=Count(
            'id',
            filter=Q(
                invoce_no__isnull=True)&
                ~Q(id__in=StockCheck.objects.filter(month__gte=first_day_of_this_month.month,year=first_day_of_this_month.year).values_list('product__id', flat=True)    

            )
            ),
        intransit=Count(
            'id',
            filter=Q(status="O")
            )
    ).values('branch__name', 'tot_purchase','uninvoiced','sale','intransit','lastmonth','thismonth')

    start_date =   first_day_of_this_month - timedelta(days=365)
    vendor = Vendor.objects.all()
    models = Model.objects.all()
    print("start_date")  
    print(start_date)  
    
    return render(request,'product/index.html',{"this_month":this_month,'summary':summary,'branch_wise':branch_wise,'vendors':vendor,'models':models})

@login_required
@check_access("branches","access")
def branch(request):
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='branches').values_list('access_string',flat=True)

    return render(request,'product/branch.html',{'access_type':access_type})

@login_required
@check_access("vendor","access")
def vendor(request):
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='vendor').values_list('access_string',flat=True)

    return render(request,'product/vendor.html',{'access_type':access_type})
@login_required
@check_access("model","access")
def model(request):
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='model').values_list('access_string',flat=True)

    return render(request,'product/model.html',{'access_type':access_type})
@login_required
@check_access("transfers","access")
def transfers(request):
    return render(request,'product/transfers.html')

@login_required
@check_access("link_invoice","access")
def invoice(request):
    return render(request,'product/invoice.html')

@login_required
@check_access("prd_report","access")
def report(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()
    models = Model.objects.all()

    return render(request,'product/report.html',{'branches':branches,'vendors':vendor,'models':models})

@login_required
# @check_access("prd_report","access")
def report_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products_report.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Purchase Id', 'Purchase Date', 'Vendor Code', 'Vendore Name','Model','Serial No','Branch Code','Branch Name','Invoice Date','Invoice Name','Customer' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
     # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    queryset = Product.objects.all()
    if request.GET.get('p_from_date', None):
        print("p_from_date")
        queryset = queryset.filter(purchase_date__gte=datetime.strptime(
            request.GET.get('p_from_date', None), '%d-%m-%Y').date())
    if request.GET.get('p_to_date', None):
        print("p_to_date")
        queryset = queryset.filter(purchase_date__lte=datetime.strptime(
            request.GET.get('p_to_date', None), '%d-%m-%Y').date())
    if request.GET.get('i_from_date', None):
        print("i_from_date")
        queryset = queryset.filter(invoice_date__gte=datetime.strptime(
            request.GET.get('i_from_date', None), '%d-%m-%Y').date())
    if request.GET.get('i_to_date', None):
        print("i_to_date")
        queryset = queryset.filter(invoice_date__lte=datetime.strptime(
            request.GET.get('i_to_date', None), '%d-%m-%Y').date())

    if request.GET.get('branch', None):
        print("branch")
        queryset = queryset.filter(
            branch__id=request.GET.get('branch', None))
    if request.GET.get('vendor', None):
        print("vendor")
        queryset = queryset.filter(
            model__vendor__id=request.GET.get('vendor', None))
    if request.GET.get('model', None):
        print("model")
        queryset = queryset.filter(
            model__id=request.GET.get('model', None))
    if request.GET.get('status', None):
        print("status")
        queryset = queryset.filter(
            status=request.GET.get('status', None))

    if request.GET.get('pur_invoce_no', None):
        print("pur_invoce_no")
        queryset = queryset.filter(
            pur_invoce_no__icontains=request.GET.get('pur_invoce_no', None))
    if request.GET.get('serial_num', None):
        print("serial_num")
        queryset = queryset.filter(
            serial_num=request.GET.get('serial_num', None))
    if request.GET.get('invoice_no', None):
        print("invoice_no")
        queryset = queryset.filter(
            invoce_no=request.GET.get('invoice_no', None))

    if request.GET.get('cust_code', None):
        print("cust_code")
        queryset = queryset.filter(
            customer_code=request.GET.get('cust_code', None))

    rows = queryset.values_list('pur_invoce_no','purchase_date','model__vendor__code','model__vendor__name','model__name','serial_num','branch__code','branch__name','invoice_date','invoce_no','customer_code')
    print(rows)
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    # rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        col = 0
        for col_num in range(len(row)):
            if col == 1 or col == 8 :
                ws.write(row_num, col_num, row[col_num], date_format)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
            col = col + 1

    wb.save(response)
    return response

@login_required
@check_access("prd_modify_del","access")
def product(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()
    models = Model.objects.all()
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='prd_modify_del').values_list('access_string',flat=True)


    return render(request,'product/product.html',{'branches':branches,'vendors':vendor,'models':models,'access_type':access_type})

@login_required
@check_access("summ_report","access")
def summ_report(request):
    first_day_of_this_month = datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    print(first_day_of_this_month)
    summary = Product.objects.values('model','branch').annotate(
    tot_purchase=Count('id'),
    uninvoiced=Count(
        'id',
        filter=Q(invoce_no__isnull=True)
        ),
    sale=Count(
        'id',
        filter=Q(invoce_no__isnull=False)
        ),
    lastmonth=Count(
        'id',
        filter=Q(
            invoce_no__isnull=True,
            purchase_date__lt=first_day_of_this_month)&
            ~Q(id__in=StockCheck.objects.filter(Q(month__lt=first_day_of_this_month.month,year=first_day_of_this_month.year)|Q(year__lt=first_day_of_this_month.year)).values_list('product__id', flat=True)    
        )
        ),
    thismonth=Count(
        'id',
        filter=Q(
            invoce_no__isnull=True)&
            ~Q(id__in=StockCheck.objects.filter(month__gte=first_day_of_this_month.month,year=first_day_of_this_month.year).values_list('product__id', flat=True)    

        )
        ),
    intransit=Count(
        'id',
        filter=Q(status="O")
        )
        ).values('model__vendor__name', 'model__vendor__code', 'model__name','branch__name', 'tot_purchase','uninvoiced','sale','intransit','lastmonth','thismonth')
    print(summary.query)
    return render(request,'product/summ_report.html',{'summary':summary})

@check_access("summ_report","access")
def stock_summ_report(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()
    models = Model.objects.all()
    months = [
        {"no":1,"text":"Jan"},
        {"no":2,"text":"Feb"},
        {"no":3,"text":"Mar"},
        {"no":4,"text":"Apr"},
        {"no":5,"text":"May"},
        {"no":6,"text":"Jun"},
        {"no":7,"text":"Jul"},
        {"no":8,"text":"Aug"},
        {"no":9,"text":"Sep"},
        {"no":10,"text":"Oct"},
        {"no":11,"text":"Nov"},
        {"no":12,"text":"Dec"},
    ]
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    print(current_month)
    years = []
    for i in range(current_year-5,current_year+5):
        years.append(i)
    
    return render(request,'product/stock_summ_report.html',{'branches':branches,'vendors':vendor,'months':months,'years':years,'current_year':current_year,'current_month':current_month,'models':models})

@login_required
@check_access("stock_rpt","access")
def stock_report(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()
    models = Model.objects.all()
    months = [
        {"no":1,"text":"Jan"},
        {"no":2,"text":"Feb"},
        {"no":3,"text":"Mar"},
        {"no":4,"text":"Apr"},
        {"no":5,"text":"May"},
        {"no":6,"text":"Jun"},
        {"no":7,"text":"Jul"},
        {"no":8,"text":"Aug"},
        {"no":9,"text":"Sep"},
        {"no":10,"text":"Oct"},
        {"no":11,"text":"Nov"},
        {"no":12,"text":"Dec"},
    ]
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    years = []
    for i in range(current_year-5,current_year+5):
        years.append(i)

    return render(request,'product/stock_report.html',{'branches':branches,'vendors':vendor,'months':months,'years':years,'current_year':current_year,'current_month':current_month,'models':models})

def forbidden(request):
    return render(request,'product/forbidden.html')


@login_required
@check_access("prd_purchase","access")
def purchase(request):
    branch = Branch.objects.all()
    models = Model.objects.all()

    return render(request,'product/purchase.html',{'branches':branch,'models':models})
@login_required
@check_access("prd_transfer","access")
def transfer(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()

    return render(request,'product/transfer.html',{'branches':branches,'vendors':vendor})

@login_required
@check_access("credit_note","access")
def credit_note(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()

    return render(request,'product/credit_note.html',{'branches':branches,'vendors':vendor})

@login_required
@check_access("branches","add")
def add_branch(request):
    if request.method == "POST":
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save()
            # print(club)
            messages.success(request,_("The Branch {branch} is created".format(branch=branch.name)))
            return redirect(reverse('branch'))

            
    else:
        form = BranchForm()
    return render(request,'product/add_branch.html',{'form':form})

@login_required
@check_access("vendor","add")
def add_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            # print(club)
            messages.success(request,_("The Branch {vendor} is created".format(vendor=vendor.name)))
            return redirect(reverse('vendor'))

            
    else:
        form = VendorForm()
    return render(request,'product/add_vendor.html',{'form':form})

@login_required
@check_access("model","add")
def add_model(request):
    if request.method == "POST":
        form = ModelForm(request.POST)
        if form.is_valid():
            model = form.save()
            # print(club)
            messages.success(request,_("The Model  {model} is created".format(model=model.name)))
            return redirect(reverse('model'))

            
    else:
        form = ModelForm()
    return render(request,'product/add_model.html',{'form':form})


@login_required
@check_access("branch","modify")
def edit_branch(request,id):
    instance = Branch.objects.get(id=id)
    if request.method == "POST":
        form = BranchForm(request.POST,instance=instance)
        if form.is_valid():
            branch = form.save()
            # print(club)
            messages.success(request,_("The Branch {branch} is Edited".format(branch=branch.name)))
            return redirect(reverse('branch'))

            
    else:
        form = BranchForm(instance=instance)
    return render(request,'product/add_branch.html',{'form':form})

@login_required
@check_access("vendor","modify")
def edit_vendor(request,id):
    instance = Vendor.objects.get(id=id)
    if request.method == "POST":
        form = BranchForm(request.POST,instance=instance)
        if form.is_valid():
            vendor = form.save()
            # print(club)
            messages.success(request,_("The Vendor {vendor} is Edited".format(vendor=vendor.name)))
            return redirect(reverse('vendor'))

            
    else:
        form = BranchForm(instance=instance)
    return render(request,'product/add_vendor.html',{'form':form})

@login_required
@check_access("model","modify")
def edit_model(request,id):
    instance = Model.objects.get(id=id)
    if request.method == "POST":
        form = ModelForm(request.POST,instance=instance)
        if form.is_valid():
            model = form.save()
            # print(club)
            messages.success(request,_("The Branch {model} is Edited".format(model=model.name)))
            return redirect(reverse('model'))

            
    else:
        form = ModelForm(instance=instance)
    return render(request,'product/add_model.html',{'form':form})

@login_required
@check_access("prd_modify_del","modify")
def edit_product(request,id):
    instance = Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST,instance=instance)
        if form.is_valid():
            model = form.save()
            # print(club)
            messages.success(request,_("The Product {model} is Edited".format(model=model.serial_num)))
            return redirect(reverse('product'))

            
    else:
        form = ProductForm(instance=instance)
    return render(request,'product/edit_product.html',{'form':form})

@login_required
@check_access("take_stock","access")
def stock_check(request):
    months = [
        {"no":1,"text":"Jan"},
        {"no":2,"text":"Feb"},
        {"no":3,"text":"Mar"},
        {"no":4,"text":"Apr"},
        {"no":5,"text":"May"},
        {"no":6,"text":"Jun"},
        {"no":7,"text":"Jul"},
        {"no":8,"text":"Aug"},
        {"no":9,"text":"Sep"},
        {"no":10,"text":"Oct"},
        {"no":11,"text":"Nov"},
        {"no":12,"text":"Dec"},
    ]
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    years = []
    for i in range(current_year-5,current_year+5):
        years.append(i)
    
    models = Model.objects.all()


    return render(request,'product/stock_check.html',{'months':months,'years':years,'current_year':current_year,'current_month':current_month,'models':models})




