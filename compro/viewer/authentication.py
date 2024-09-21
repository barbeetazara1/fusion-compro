from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model, logout
from app.models import Users
from django.http import JsonResponse, HttpResponseRedirect
from services import odoo

from services.logger import logger

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
            logger.info('Authentication POST API')
            username = request.POST.get('username')
            passw = request.POST.get('password')
            
            odoo_sts, data, cookie = odoo.authenticate(username, passw)
            
            if (odoo_sts):                  
                logger.info(f'Odoo user logged in - {cookie['session_id']} - (deprecated)')
                resp = JsonResponse({'status': True, 'data':{'merchant': 'odoo', 'odoo_session': cookie['session_id'], 'odoo_uid': data['result']['uid']}})     
                return resp
            
            user = authenticate(request=request, username=username, password=passw)
            logger.info(f'Fusion user auth - {username}')
            if user:                
                try:
                    login(request, user)
                    logger.info(f'Fusion user logged in.')
                    return JsonResponse({'status': True, 'data':{'merchant': 'fusion', 'redirect_url': str(redirect("main-dashboard").url)}})     
                except Exception as login_eror:
                    logger.error(f'Fusion user error while login() - {login_eror}')
                    print('Error when try login', login_eror)
                    return JsonResponse({'status': False, 'data':{'merchant': 'fusion', 'redirect_url': str(redirect("main-dashboard").url)}})
            else:
                logger.error(f'Fusion user not found - {username}')
                return JsonResponse({'status': False, 'data':{'merchant': 'fusion', 'msg': 'Tidak ada user ditemukan.'}})


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
