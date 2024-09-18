from django.shortcuts import render
from django.conf import settings
from .models import OwnerProfile

def index(request):
    ctx = {}            
    all_profile = OwnerProfile.objects.all()
    for profile_item in all_profile:
        ctx[profile_item.info] = profile_item.content   
    resp = render(template_name='index.html', request=request, context=ctx)
    return resp