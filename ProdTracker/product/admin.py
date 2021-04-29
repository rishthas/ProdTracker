from django.contrib import admin
from .models import Branch,Product,Transfer,Vendor,Model
# Register your models here.

admin.site.register(Branch)
admin.site.register(Product)
admin.site.register(Transfer)
admin.site.register(Vendor)
admin.site.register(Model)
