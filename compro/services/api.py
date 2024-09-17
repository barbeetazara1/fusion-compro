from django.conf import settings
from django.views import View
from django.http import JsonResponse
from app.models import Visitor
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
                


