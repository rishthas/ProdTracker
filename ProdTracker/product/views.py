from django.shortcuts import render,redirect
from .forms import BranchForm,VendorForm,ModelForm
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext as _
from .models import Branch, Vendor, Product, Transfer, StockCheck,Model
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.models import RoleAccess
from django.db.models import Count, Q






# Create your views here.
@login_required
def index(request):
    this_month = datetime.today().strftime("%b-%Y")
    
    return render(request,'product/index.html',{"this_month":this_month})

@login_required
def branch(request):
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='branches').values_list('access_string',flat=True)

    return render(request,'product/branch.html',{'access_type':access_type})

@login_required
def vendor(request):
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='vendor').values_list('access_string',flat=True)

    return render(request,'product/vendor.html',{'access_type':access_type})
@login_required
def model(request):
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='model').values_list('access_string',flat=True)

    return render(request,'product/model.html',{'access_type':access_type})
@login_required
def transfers(request):
    return render(request,'product/transfers.html')
@login_required
def invoice(request):
    return render(request,'product/invoice.html')
@login_required
def report(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()
    models = Model.objects.all()

    return render(request,'product/report.html',{'branches':branches,'vendors':vendor,'models':models})

@login_required
def summ_report(request):
    first_day_of_this_month = datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    print(first_day_of_this_month)
    summary = Product.objects.values('model').annotate(
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
        )
        ).values('model__vendor__name', 'model__vendor__code', 'model__name', 'tot_purchase','uninvoiced','sale','lastmonth','thismonth')
    print(summary.query)
    return render(request,'product/summ_report.html',{'summary':summary})

@login_required
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

@login_required
def purchase(request):
    branch = Branch.objects.all()
    models = Model.objects.all()

    return render(request,'product/purchase.html',{'branches':branch,'models':models})
@login_required
def transfer(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()

    return render(request,'product/transfer.html',{'branches':branches,'vendors':vendor})

@login_required
def credit_note(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()

    return render(request,'product/credit_note.html',{'branches':branches,'vendors':vendor})

@login_required
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




