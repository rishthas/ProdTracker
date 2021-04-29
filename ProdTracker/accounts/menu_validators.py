from .models import RoleAccess
def has_menu_access(request,ref):
    print("INside has_menu_access {}".format(ref))
    print(RoleAccess.objects.filter(role=request.user.profile.role_id,access_point=ref))
    if RoleAccess.objects.filter(role=request.user.profile.role_id,access_point=ref):
        print("True")
        return True
    else:
        print("False")
        return False