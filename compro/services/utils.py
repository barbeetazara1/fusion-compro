from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.conf import settings
import os, json

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            _deny_page = render(request, 'base/403.html')
            _deny_page.status_code = 403
            return _deny_page
        return _wrapped_view
    return decorator


def read_json(filename):
    # Buat path lengkap ke file JSON
    file_path = os.path.join(settings.BASE_DIR, f'{filename}')
    
    # Baca file JSON
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    else:
        print("Error when try unpacking configuration file.")
        return {}
    


    
