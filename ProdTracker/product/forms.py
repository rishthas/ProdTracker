from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Branch,Vendor

class BranchForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Branch Name')}),max_length=50, label=_("Branch Name"))
    code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Branch Code')}),max_length=50, label=_("Branch Code"))

    class Meta:
        model = Branch
        fields = "__all__"


class VendorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Vendor Name')}),max_length=50, label=_("Vendor Name"))
    code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Vendor Code')}),max_length=50, label=_("Vendor Code"))

    class Meta:
        model = Vendor
        fields = "__all__"

