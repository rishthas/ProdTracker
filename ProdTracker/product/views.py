from django.shortcuts import render,redirect
from .forms import BranchForm,VendorForm
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext as _
from .models import Branch,Vendor
from datetime import datetime



# Create your views here.
def index(request):
    return render(request,'product/index.html')


def branch(request):
    return render(request,'product/branch.html')


def vendor(request):
    return render(request,'product/vendor.html')

def transfers(request):
    return render(request,'product/transfers.html')

def invoice(request):
    return render(request,'product/invoice.html')

def report(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()

    return render(request,'product/report.html',{'branches':branches,'vendors':vendor})


def stock_report(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()
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

    return render(request,'product/stock_report.html',{'branches':branches,'vendors':vendor,'months':months,'years':years,'current_year':current_year,'current_month':current_month})


def purchase(request):
    branch = Branch.objects.all()
    vendor = Vendor.objects.all()

    return render(request,'product/purchase.html',{'branchs':branch,'vendors':vendor})

def transfer(request):
    branches = Branch.objects.all()
    vendor = Vendor.objects.all()

    return render(request,'product/transfer.html',{'branches':branches,'vendors':vendor})


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


def edit_vendor(request,id):
    instance = Vendor.objects.get(id=id)
    if request.method == "POST":
        form = BranchForm(request.POST,instance=instance)
        if form.is_valid():
            vendor = form.save()
            # print(club)
            messages.success(request,_("The Branch {vendor} is Edited".format(vendor=vendor.name)))
            return redirect(reverse('vendor'))

            
    else:
        form = BranchForm(instance=instance)
    return render(request,'product/add_vendor.html',{'form':form})


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
    
    vendor = Vendor.objects.all()


    return render(request,'product/stock_check.html',{'months':months,'years':years,'current_year':current_year,'current_month':current_month,'vendors':vendor})