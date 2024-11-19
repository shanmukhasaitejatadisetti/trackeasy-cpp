from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.view_order, name='view_order'),
    path('orders/manage/', views.manage_orders, name='manage_orders'),
    path('order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
]