from django.urls import path
from . import views

urlpatterns = [

    path(
        '<int:order_id>/',views.payment_view,name='payment'),

    path(
        'receipt/<int:order_id>/',views.receipt_view,name='receipt'),

]