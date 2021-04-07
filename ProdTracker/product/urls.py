from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="home"),
    path('branch/', views.branch,name="branch"),
    path('vendor/', views.vendor,name="vendor"),
    path('purchase/', views.purchase,name="purchase"),
    path('branch/add', views.add_branch,name="add-branch"),
    path('vendor/add', views.add_vendor,name="add-vendor"),
    path('branch/edit/<int:id>/', views.edit_branch,name="edit-branch"),
    path('vendor/edit/<int:id>/', views.edit_vendor,name="edit-vendor"),
    # path('login/',views.login_page,name="login"),
]