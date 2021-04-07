from django.shortcuts import render,redirect
from .forms import BranchForm,VendorForm
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext as _
from .models import Branch,Vendor



# Create your views here.
def index(request):
    return render(request,'product/index.html')


def branch(request):
    return render(request,'product/branch.html')


def vendor(request):
    return render(request,'product/vendor.html')

def purchase(request):
    branch = Branch.objects.all()
    vendor = Vendor.objects.all()

    return render(request,'product/purchase.html',{'branchs':branch,'vendors':vendor})


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