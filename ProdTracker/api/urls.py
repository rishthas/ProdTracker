from django.urls import path,include
from rest_framework import routers
from .views import BranchViewSet,VendorViewSet,ProductViewSet,TransferViewSet

router = routers.DefaultRouter()
router.register('branch',BranchViewSet)
router.register('vendor',VendorViewSet)
router.register('product',ProductViewSet)
router.register('transfer',TransferViewSet)



urlpatterns =[
    path('',include(router.urls))
]