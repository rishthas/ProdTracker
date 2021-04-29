from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import Role 

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm  ','placeholder': 'User Name'}),help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm  ','placeholder':'Password'}),label='Password',help_text="Please enter the required password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm  ','placeholder':'Password'}),label='Confirm Password',help_text="Please re-enter the password")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm  ','placeholder':'First Name'}),max_length=30, required=True, )
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm  ','placeholder':'First Name'}),max_length=30, required=False, )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm  '}),max_length=254, help_text='Required. Inform a valid email address.')
    role_id = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control form-control-sm  ',}),required=True,queryset=Role.objects.filter().all())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role_id')

class EditUserForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm  ','placeholder': 'User Name','readonly':'true'}),help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm  ','placeholder':'First Name'}),max_length=30, required=True, )
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm  ','placeholder':'First Name'}),max_length=30, required=False, )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm  '}),max_length=254, help_text='Required. Inform a valid email address.')
    role_id = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control form-control-sm  ',}),required=True,queryset=Role.objects.all())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','role_id')