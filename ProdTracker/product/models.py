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


class Model(models.Model):
    name = models.CharField(_("Vendor Name"), max_length=50)
    vendor = models.ForeignKey(Vendor, verbose_name=_("Vendor"), on_delete=models.CASCADE,related_name='vendor')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Model'
        verbose_name_plural = 'Models'
  

class Product(models.Model):
    serial_num = models.CharField(_("Serial Number"), max_length=200)
    # vendor = models.ForeignKey(Vendor, verbose_name=_("Vendor"), on_delete=models.CASCADE)
    # model_no = models.CharField(_("Model No"), max_length=50) 
    model = models.ForeignKey(Model, verbose_name=_("Model"), on_delete=models.CASCADE)
    pur_invoce_no = models.CharField(_("Purchase Invoice Number"), max_length=50,null=True,blank=True)
    purchase_date = models.DateField(_("Purchase Date"), auto_now=False, auto_now_add=False)   
    branch = models.ForeignKey(Branch, verbose_name=_("Branch"), on_delete=models.SET_NULL,null=True,blank=True)
    invoice_date = models.DateField(_("Invoice Date"),null=True,blank=True)
    invoce_no = models.CharField(_("Invoice Number"), max_length=50,null=True,blank=True)
    customer_code = models.CharField(_("Customer Code"), max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        unique_together=('model','serial_num')

    def __str__(self):
        return self.serial_num

    # def get_absolute_url(self):
    #     return reverse("Product_detail", kwargs={"pk": self.pk})

class Transfer(models.Model):

    date = models.DateField(_("Date"), auto_now=False, auto_now_add=False)    
    branch = models.ForeignKey(Branch, verbose_name=_("Branch"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    status = models.CharField(_("Status"), max_length=50,choices=(("I","In"),("O","Out")))
    remark = models.CharField(_("Remarks"), max_length=100,null=True,blank=True)
    event_time = models.DateTimeField(_("Event Time"), auto_now=True, auto_now_add=False)
    class Meta:
        verbose_name = _("Transfer")
        verbose_name_plural = _("Transfers")

    def __str__(self):
        return self.name



class StockCheck(models.Model):
    
    month = models.IntegerField(_("Month"))
    year = models.IntegerField(_("Year"))
    event_time = models.DateTimeField(_("Event Time"), auto_now=True, auto_now_add=False)
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)


    

    class Meta:
        verbose_name = _("StockCheck")
        verbose_name_plural = _("StockChecks")

    def __str__(self):
        return "{}_{}_{}".format(self.product.serial_num,self.month,self.year)

