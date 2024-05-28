from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # 主页的URL模式
    path('add/', views.add_contact, name='add_contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact_list/', views.contact_list, name='contact_list'),  # 添加这一行
    path('edit/<int:contact_id>/', views.edit_contact_detail, name='edit_contact'),
    path('delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('search/', views.search_results, name='search_results'),
]
