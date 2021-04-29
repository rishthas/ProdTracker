from django.urls import path
from . import views

urlpatterns = [
    
    path('roles/', views.roles,name="roles"),
    path('users/', views.users,name="users"),
    path('signup/', views.sign_up,name="sign-up"),
    path('role/add/', views.add_roles,name="add-role"),
    path('role/edit/<int:id>/', views.edit_roles,name="edit-role"),
    path('user/edit/<int:id>/', views.edit_user,name="edit-user"),

    
    # path('login/',views.login_page,name="login"),
]