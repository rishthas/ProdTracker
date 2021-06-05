from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Branch,Vendor,Model,Product

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


class ModelForm(forms.ModelForm):
    
    vendor = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control form-control-sm  ',}),required=True,queryset=Vendor.objects.filter().all())
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Model')}),max_length=50, label=_("Model Name"))

    class Meta:
        model = Model
        fields = "__all__"

class ProductForm(forms.ModelForm):
    serial_num = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Serial Number')}),max_length=50, label=_("Serial Number"))
    model = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control form-control-sm  ',}),required=True,queryset=Model.objects.filter().all())
    pur_invoce_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Purchase Invoice Number')}),max_length=50, label=_("Purchase Invoice Number"))
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder': _('Purchase Date')}), label=_("Purchase Date"))
    branch = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control form-control-sm  ',}),required=True,queryset=Branch.objects.filter().all())
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder': _('Invoice Date')}), label=_("Invoice Date"),required=False)
    invoce_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Invoice Number')}),max_length=50, label=_("Invoice Number"),required=False)
    customer_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': _('Customer Code')}),max_length=50, label=_("Customer Code"),required=False)

    class Meta:
        model = Product
        fields = ['serial_num', 'model', 'pur_invoce_no', 'purchase_date','branch','invoice_date','invoce_no','customer_code']

