from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model, logout
from app.models import Users
from django.http import JsonResponse, HttpResponseRedirect
from services import odoo

class Authentication(View):
    
    context = ''

    def get(self, request, *args, **kwargs):
        
        if (self.context == 'login'):
            if (request.user.is_authenticated):
                return redirect('main-dashboard')
            resp = render(template_name='login.html', request=request)
            return resp
        if (self.context == 'logout'):
            logout(request)
            return redirect('landing')
        
    def post(self, request, *args, **kwargs):
        
        if (self.context == 'login'):
            username = request.POST.get('username')
            passw = request.POST.get('password')
            odoo_sts, data, cookie = odoo.authenticate(username, passw)
            
            if (odoo_sts):
                # Menyimpan informasi pengguna di Django
                uid = data['result']['uid']
                user_name = data['result']['name']
                db = data['result']['db']
                # Menyimpan informasi sesi di Django
                request.session['odoo_user_id'] = uid
                request.session['odoo_username'] = user_name
                request.session['odoo_db'] = db

                cookie_data = {o_cook.name: o_cook.value for o_cook in cookie}
                # Mengarahkan pengguna ke Odoo
                redirect_url = f"https://{settings.ODOO_URL}/web"
                response_redirect = HttpResponseRedirect(redirect_url)
                # Atur cookie untuk domain Odoo
                for coo in cookie:
                    response_redirect.set_cookie(
                        coo.name,
                        coo.value,
                        httponly=True,
                        secure=True,
                        domain='odoo.internal-fusion-erp.site',
                        path='/',
                        samesite='None'
                    )
                return response_redirect
            
            user = authenticate(request=request, username=username, password=passw)
            if user:                
                try:
                    login(request, user)
                    return JsonResponse({'status': True, 'data':{'merchant': 'fusion'}})     
                except Exception as login_eror:
                    print('Error when try login', login_eror)
                    return JsonResponse({'status': False, 'data':{'msg': 'Internal server error'}})     
            else:
                return JsonResponse({'status': False, 'data':{'msg': 'User/Password salah'}})     


        if (self.context == 'register'):
            username = request.POST.get('username')
            passw = request.POST.get('password')
            confirm_passw = request.POST.get('password-confirm')
            role = request.POST.get('role')
            email = request.POST.get('email')
            
            user_model = get_user_model()
            if (len(username) > 7 and len(passw) > 8):        
                try:
                    new_user = user_model.objects.create_user(username=username, password=passw)
                    new_user.role = role
                    new_user.email = email
                    new_user.save()
                    return JsonResponse({'status': True, 'data':{'msg': 'Login berhasil'}})
                except Exception as failed_create_user:
                    print(f'Failed create user : {failed_create_user}')
                    return JsonResponse({'status': False, 'data':{'msg': 'Server maintenance (500 Internal Server)'}})
            else:
                print(f'Invalid username - {username}')
                return JsonResponse({'status': False, 'data':{'msg': 'Username/password terlalu pendek'}})
