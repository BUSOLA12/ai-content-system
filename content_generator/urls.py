# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('content/<uuid:content_id>/', views.content_detail, name='content_detail'),
    path('content/<uuid:content_id>/vote/', views.vote_content, name='vote_content'),
    path('notifications/', views.notifications, name='notifications'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='ai_content/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    
    # # API endpoints
    # path('api/generate-content/', views.generate_content, name='generate_content_api'),
    # path('api/content/<uuid:content_id>/vote/', views.api_vote_content, name='api_vote_content'),
    # path('api/notifications/', views.api_notifications, name='api_notifications'),
]