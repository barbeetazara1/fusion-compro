from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.conf import settings
import os, json, re


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

def is_valid_phone_number(phone_number):
    pattern = r"^08\d{8,11}$"
    if re.match(pattern, phone_number):
        if (len(str(phone_number)) < 12 > 14):
            return False, None
        return True, phone_number
    return False, None


def is_valid_name(name):
    # Regex untuk memvalidasi nama
    pattern = r"^[A-Za-z\s]+$"
    if re.match(pattern, name):
        # Mengembalikan True dan nama dengan huruf kapital di awal setiap kata
        capitalized_name = ' '.join(word.capitalize() for word in name.split())
        return True, capitalized_name
    return False, None


# Fungsi untuk memvalidasi email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True, email
    return False, None
