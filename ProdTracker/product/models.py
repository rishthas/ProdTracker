from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Branch(models.Model):
    name = models.CharField(_("Branch Name"), max_length=50)
    code = models.CharField(_("Branch Code"), max_length=50)
    

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branchs")

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(_("Vendor Name"), max_length=50)
    code = models.CharField(_("Vendor Code"), max_length=50)
    

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Vendor_detail", kwargs={"pk": self.pk})
  

class Product(models.Model):
    serial_num = models.CharField(_("Serial Number"), max_length=200)
    vendor = models.ForeignKey(Vendor, verbose_name=_("Vendor"), on_delete=models.CASCADE)
    model_no = models.CharField(_("Model No"), max_length=50) 
    purchase_date = models.DateField(_("Purchase Date"), auto_now=False, auto_now_add=False)   
    branch = models.ForeignKey(Branch, verbose_name=_("Branch"), on_delete=models.SET_NULL,null=True,blank=True)
    invoce_no = models.CharField(_("Invoice Number"), max_length=50,null=True,blank=True)
    customer_code = models.CharField(_("Customer Code"), max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        unique_together=('vendor','model_no','serial_num')

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Product_detail", kwargs={"pk": self.pk})

class Transfer(models.Model):

    date = models.DateField(_("Date"), auto_now=False, auto_now_add=False)    
    branch = models.ForeignKey(Branch, verbose_name=_("Branch"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    status = models.CharField(_("Status"), max_length=50,choices=(("I","In"),("O","Out")))
    class Meta:
        verbose_name = _("Transfer")
        verbose_name_plural = _("Transfers")

    def __str__(self):
        return self.name

