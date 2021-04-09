from django.urls import path,include
from rest_framework import routers
from .views import BranchViewSet,VendorViewSet,ProductViewSet,TransferViewSet,ProductAggViewSet

router = routers.DefaultRouter()
router.register('branch',BranchViewSet)
router.register('vendor',VendorViewSet)
router.register('product',ProductViewSet)
router.register('transfer',TransferViewSet)
router.register('product_agg',ProductAggViewSet)



urlpatterns =[
    path('',include(router.urls))
]