from django.shortcuts import render
from django.conf import settings
from .models import OwnerProfile
from django.http import JsonResponse, HttpResponseRedirect

def index(request):
    ctx = {}            
    all_profile = OwnerProfile.objects.all()
    for profile_item in all_profile:
        ctx[profile_item.info] = profile_item.content   
    resp = render(template_name='index.html', request=request, context=ctx)
    return resp

def check_trial_status(request):
    if request.method == 'GET':
        # Logika untuk memeriksa status trial
        user_id = request.GET.get('email')

        trial_status = True

        return JsonResponse({
            'status': False,
            'data': {
                'msg': '200' if trial_status else 'Trial expired'
            }
        })
    
    return JsonResponse({'status': False, 'data': {'msg': 'Invalid request'}}, status=400)
