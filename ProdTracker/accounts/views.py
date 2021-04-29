from django.shortcuts import render,redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Role,RoleAccess
from .forms import SignUpForm,EditUserForm
from django.contrib import messages
from django.contrib.auth.models import User




# Create your views here.
@login_required
def users(request):
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='user_management').values_list('access_string',flat=True)

    return render(request,'registration/users.html',{'access_type':access_type})

@login_required
def sign_up(request):
    context = {}
    form = SignUpForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.role_id = form.cleaned_data.get('role_id')
            user.save()
            # login(request,user)
            # return render(request,'accounts/index.html')
            messages.success(
                request, "The User is successfully created.")
            return redirect(reverse('users'))
    context['form']=form
    return render(request,'registration/sign_up.html',context)

@login_required
def edit_user(request,id):
    context = {}
    instance = User.objects.get(id=id)
    form = EditUserForm(request.POST or None,instance=instance,initial={'role_id': instance.profile.role_id})
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.role_id = form.cleaned_data.get('role_id')
            user.save()
            # login(request,user)
            # return render(request,'accounts/index.html')
            messages.success(
                request, "The User is successfully Edited.")
            return redirect(reverse('users'))
    context['form']=form
    context["role_id"] = instance.profile.role_id
    return render(request,'registration/edit_user.html',context)

@login_required
def roles(request):
    access_type = RoleAccess.objects.filter(role = request.user.profile.role_id,access_point='role_management').values_list('access_string',flat=True)
    return render(request,'registration/roles.html',{'access_type':access_type})

@login_required
def add_roles(request):
    """
    View for routig to the club home page. 
    
    Keyword arguments:
    request -- http requests, 
    Return: template for culb home.
    """
   
    return render(request,'registration/add_roles.html',{"menu_settings":settings.ADMIN_MENU})

@login_required
def edit_roles(request,id):
    """
    View for routig to the club home page. 
    
    Keyword arguments:
    request -- http requests, 
    Return: template for culb home.
    """
    role = Role.objects.get(id=id)
    # role_access = ClubRoleAccess.objects.get(role=role)
   
    return render(request,'registration/edit_roles.html',{"menu_settings":settings.ADMIN_MENU,"role":role})
