from functools import wraps
from django.conf import settings
from apps.models import Visitor
import os, json


def record_visitor(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        ip_address = request.META.get('REMOTE_ADDR')                        
        user_agent = request.META.get('HTTP_USER_AGENT')            
        path = str(request.path)
        Visitor.objects.create(ip_address=ip_address, user_agent=user_agent, path=path)         
        return view_func(request, *args, **kwargs)
    return wrapper