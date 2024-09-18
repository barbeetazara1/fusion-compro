from django.urls import path
from . import views
from viewer.news import News
from viewer.dashboard import Dashboard
from viewer.settings import UserConfigurations, OwnerConfigurations
from viewer.authentication import Authentication
from services.api import API

urlpatterns = [
    path('', views.index, name='landing'),
    path('trial/', views.check_trial_status, name='check-trial-status'),
    path('dashboard/', Dashboard.as_view(context='main-dashboard'), name='main-dashboard'),
    path('dashboard/partner/', Dashboard.as_view(context='partner-dashboard'), name='partner-dashboard'),
    path('dashboard/partner/create-new/', Dashboard.as_view(context='new-partner'), name='new-partner'),
    path('dashboard/partner/delete/', Dashboard.as_view(context='delete-partner'), name='delete-partner'),
    path('dashboard/news/', Dashboard.as_view(context='news-dashboard'), name='news-dashboard'),
    path('dashboard/news/create-new/', Dashboard.as_view(context='create-news-dashboard'), name='create-news-dashboard'),
    path('dashboard/news/<int:article_id>/edit/', Dashboard.as_view(context='edit-news-dashboard'), name='edit-news-dashboard'),
    path('news/', News.as_view(context='news'), name='news'),
    path('news/<int:article_id>/', News.as_view(context='news-detail'), name='news-detail'),
    path('owner-configuration/', OwnerConfigurations.as_view(context='owner-configuration'), name='owner-configuration'),
    path('main-profile/', OwnerConfigurations.as_view(context='main-profile'), name='main-profile'),
    path('user-configuration/', UserConfigurations.as_view(context='user-list'), name='user-list'),
    path('login/', Authentication.as_view(context='login'), name='login'),
    path('trial/', Authentication.as_view(context='trial'), name='trial'),
    path('logout/', Authentication.as_view(context='logout'), name='logout'),
    path('register/', Authentication.as_view(context='register'), name='register'),

    # API Based
    path('api/visitor/', API.as_view(context='api-visitor'), name='api-visitor'),
    path('api/reporter/', API.as_view(context='api-reporter'), name='api-reporter'),
]