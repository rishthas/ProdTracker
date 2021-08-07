from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="home"),
    path('forbidden/', views.forbidden,name="forbidden"),
    path('branch/', views.branch,name="branch"),
    path('vendor/', views.vendor,name="vendor"),
    path('model/', views.model,name="model"),
    path('product/', views.product,name="product"),
    path('purchase/', views.purchase,name="purchase"),
    path('stock/', views.stock_check,name="stock"),
    path('report/', views.report,name="report"),
    path('report/summary', views.summ_report,name="summ-report"),
    path('report/stock/summary', views.stock_summ_report,name="stock-summ-report"),
    path('report/stocks', views.stock_report,name="stock-report"),
    path('transfer/', views.transfer,name="transfer"),
    path('invoice/', views.invoice,name="invoice"),
    path('transfers/', views.transfers,name="transfers"),
    path('credit_note/', views.credit_note,name="credit_note"),
    path('branch/add', views.add_branch,name="add-branch"),
    path('vendor/add', views.add_vendor,name="add-vendor"),
    path('model/add', views.add_model,name="add-model"),
    path('branch/edit/<int:id>/', views.edit_branch,name="edit-branch"),
    path('vendor/edit/<int:id>/', views.edit_vendor,name="edit-vendor"),
    path('model/edit/<int:id>/', views.edit_model,name="edit-model"),
    path('product/edit/<int:id>/', views.edit_product,name="edit-product"),
    # path('login/',views.login_page,name="login"),
]