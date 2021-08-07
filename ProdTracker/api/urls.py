from django.urls import path,include
from rest_framework import routers
from .views import BranchViewSet,VendorViewSet,ProductViewSet,TransferViewSet,ProductAggViewSet,StockCheckViewSet,UserViewSet,RoleViewSet,ModelViewSet
from .views import StockSummaryViewSet
router = routers.DefaultRouter()
router.register('branch',BranchViewSet)
router.register('vendor',VendorViewSet)
router.register('product',ProductViewSet)
router.register('transfer',TransferViewSet)
router.register('product_agg',ProductAggViewSet)
router.register('stock_summ',StockSummaryViewSet)
router.register('stock_check',StockCheckViewSet)
router.register('user',UserViewSet)
router.register('roles',RoleViewSet)
router.register('model',ModelViewSet)




urlpatterns =[
    path('',include(router.urls))
]