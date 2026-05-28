from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('manage/', views.manage_orders, name='manage_orders'),
    path('update/<int:id>/', views.update_order_status, name='update_order_status'),
]