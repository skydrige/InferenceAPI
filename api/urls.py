from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api', views.index, name='index'),
    path('sample', views.test, name='test'),
    path('summary', views.direct_summary, name='directSummary'),
    path('chat', views.chat, name='chat'),
    path('logout', views.logout_view, name='logout_view'),
    path('login', views.login_view, name='login_view'),
    path('signup', views.signup, name='signup'),
    path('query', views.user_query, name='user_query'),
    path('new', views.new_chat, name='new_chat'),
    path('testing', views.test_html, name='test_html'),
    path('change/<str:session_id>', views.change_session, name='change_session'),
]
