from django.utils.deprecation import MiddlewareMixin
from .permissions import is_supportpanel_user
from .models import AdminActivityLog
import json




class SupportPanelActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user


        if not user.is_authenticated or not is_supportpanel_user(user):
            return None
        

        if request.method not in ["POST", "PUT", "PATCH", "DELETE"]:
            return None
        

        try:
            body_data = ""
            if request.body:
                body_data = request.body.decode("utf-8")

                try:
                    parsed = json.loads(body_data)
                    body_data = json.dumps(parsed)[:1000]
                except json.JSONDecodeError:
                    body_data = body_data[:500]#fallback

            AdminActivityLog.objects.create(
                admin_user=user,
                action=f"{request.method} {request.path}",
                detail=body_data,
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"), 
            )   
        except Exception:
            pass

        return None
             
                        

