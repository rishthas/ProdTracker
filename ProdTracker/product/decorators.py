from django.http import HttpResponse
from django.shortcuts import redirect
from accounts.models import RoleAccess
def check_access(arg1,arg2):

    def _method_wrapper(view_method):

        def _arguments_wrapper(request, *args, **kwargs) :
            """
            Wrapper with arguments to invoke the method
            """

            #do something with arg1 and arg2
            print("in decorator  {}  {}".format(arg1,arg2))
            if arg2 == "access":
                if RoleAccess.objects.filter(role=request.user.profile.role_id,access_point=arg1):
                    print("Has access")
                    return view_method(request, *args, **kwargs)
                else:
                    print("False")
                    return redirect("forbidden")
            else:
                if RoleAccess.objects.filter(role=request.user.profile.role_id,access_point=arg1,access_string=arg2):
                    print("Has access")
                    return view_method(request, *args, **kwargs)
                else:
                    print("False")
                    return redirect("forbidden")
                
            
            

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper

