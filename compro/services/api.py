from django.conf import settings
from django.views import View
from django.http import JsonResponse
from app.models import Visitor
from services.utils import is_valid_name, is_valid_phone_number, is_valid_email
from django.utils import timezone
from datetime import timedelta
import datetime


class API(View):
    
    context = ''

    def get(self, request, *args, **kwargs):
        resp = JsonResponse({'status': False, 'data':{'msg': '403 Forbidden'}})     
        resp.status_code = 403
        return resp
        
    def post(self, request, *args, **kwargs):
        
        if (self.context == 'api-reporter'):
            
            if (str(request.user) == 'AnonymousUser'):
                try:
                    ip_address = request.META.get('REMOTE_ADDR')                        
                    user_agent = request.META.get('HTTP_USER_AGENT')            
                    path = str(request.POST.get('path'))
                    Visitor.objects.create(ip_address=ip_address, user_agent=user_agent, path=path)   
                    return JsonResponse({'status': True, 'data': {'msg': 'Successfully report'}})     
                except Exception as error_report_visitor:
                    print(f'Error report visitor {error_report_visitor}')
                    return JsonResponse({'status': False, 'data': {'msg': 'Fail report'}})     
            else:
                print('Record skipped, because doesnot user public.')
                return JsonResponse({'status': False, 'data': {'msg': 'Youre not visitor!'}})     
                

        if (self.context == 'api-visitor'):
            req_range = request.POST.get('data-range')
            now = timezone.now().date()

            visitor_weekly_graph = []

            if (req_range == 'monthly'):
                for day in range(30):
                    date = now - timedelta(days=day)
                    visitor_count = Visitor.objects.filter(visited_at__date=date).count()  # Hitung pengunjung per hari
                    visitor_weekly_graph.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'count': visitor_count
                    })   
                visitor_weekly_graph = sorted(visitor_weekly_graph, key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'))
                
            if (req_range == 'weekly'):
                for day in range(7):
                    date = now - timedelta(days=day)
                    visitor_count = Visitor.objects.filter(visited_at__date=date).count()  # Hitung pengunjung per hari
                    visitor_weekly_graph.append({
                        'date': date.strftime('%d %B'),
                        'count': visitor_count
                    })   
                visitor_weekly_graph = sorted(visitor_weekly_graph, key=lambda x: datetime.datetime.strptime(x['date'], '%d %B'))
                
            return JsonResponse({'status': True, 'data': visitor_weekly_graph})     
                

        if (self.context == 'api-client-inbox'):
            try:
                ip_address = request.META.get('REMOTE_ADDR')                        
                user_agent = request.META.get('HTTP_USER_AGENT')    
                subject = request.POST['name']                    
                email = request.POST['email']                                            
                phone_input = request.POST['phone']                    
                try:
                    valid_name, name_capital = is_valid_name(subject)

                    if not valid_name:
                        return JsonResponse({
                            'status': False, 
                            'data': {'msg': 'Nama invalid, pastikan menggunakan nama yang sesuai.'}
                        })

                    _valid, phone = is_valid_phone_number(phone_input)
                    if not _valid:
                        return JsonResponse({
                            'status': False, 
                            'data': {'msg': 'Nomor invalid, pastikan nomor yang di input valid. Ex: 081xxxxxx'}
                        })

                    __valid, email = is_valid_email(email)
                    if not __valid:
                        return JsonResponse({
                            'status': False, 
                            'data': {'msg': 'Email invalid, pastikan alamat email yang diinput valid.'}
                        })

                    # new_inbox = ClientInbox(ip_address=ip_address, user_agent=user_agent, subject=name_capital, phone_number=phone, message=desc)
                    # new_inbox.save()
                    # logger.info(f'New inbox client from {ip_address} / name : {name_capital}')
                    
                    return JsonResponse({
                        'status': True, 
                        'data': {'msg': 'Berhasil upload form, tunggu sampai kami menghubungi Anda.'}
                    })

                except Exception as error_models:
                    # logger.error(f'Terjadi masalah saat akan menyimpan inbox ke database - {error_models}')
                    return JsonResponse({
                        'status': False, 
                        'data': {'msg': 'Fail report'}
                    })
   
            except Exception as error:
                # logger.error(f'API Client Inbox bermasalah pada data request - {error}')
                return JsonResponse({'status': False, 'data': {'msg': 'Data invalid, please check your form or reload page.'}})

