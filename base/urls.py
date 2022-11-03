from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signUp_Page, name='sign_up'),
    path('login', views.login_Page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('chat/<slug:slug>', views.chat, name='chat'),
    path('newfriend/', views.add_friend, name='add_friend'),
    path('profile/<slug:slug>', views.profile, name='profile'),
    path('messages', views.messages, name='messages')
    
]