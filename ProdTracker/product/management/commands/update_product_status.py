from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from product.models import Product
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(_('Updating the Product Status') ))
        cnt = 0
        for product in Product.objects.filter(invoce_no__isnull=False):
            product.status="S"
            product.save()
            cnt = cnt + 1
        self.stdout.write(self.style.NOTICE(_('Updated the Status for {} product'.format(cnt)) ))


            
