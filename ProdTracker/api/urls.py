from django.urls import path,include
from rest_framework import routers
from .views import BranchViewSet,VendorViewSet,ProductViewSet,TransferViewSet,ProductAggViewSet,StockCheckViewSet

router = routers.DefaultRouter()
router.register('branch',BranchViewSet)
router.register('vendor',VendorViewSet)
router.register('product',ProductViewSet)
router.register('transfer',TransferViewSet)
router.register('product_agg',ProductAggViewSet)
router.register('stock_check',StockCheckViewSet)



urlpatterns =[
    path('',include(router.urls))
]