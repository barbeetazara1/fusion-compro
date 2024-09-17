from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from app.models import Article



class News(View):
    
    context = ''

    def get(self, request, *args, **kwargs):
        
        if (self.context == 'news'):
            ctx = {
                'app_alias_name': settings.APP_ALIAS_NAME,
                'app_index_subtitle': settings.APP_INDEX_SUBTITLE,
                'email': settings.EMAIL,
                'company_address': settings.COMPANY_ADDRESS
                }
            resp = render(template_name='news.html', request=request, context=ctx)
            return resp
        
        if (self.context == 'news-detail'):
            ctx = {
                'app_alias_name': settings.APP_ALIAS_NAME,
                'app_index_subtitle': settings.APP_INDEX_SUBTITLE,
                'email': settings.EMAIL,
                'company_address': settings.COMPANY_ADDRESS
                }
            try:
                news = Article.objects.get(id=int(self.kwargs.get('article_id')))
                ctx['news'] = news
                resp = render(template_name='news.html', request=request, context=ctx)
            except Exception as error_data:
                print(error_data)
                resp = redirect('landing')                
                
            return resp