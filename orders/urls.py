from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('dostavka/', views.dostavka, name='dostavka'),
    path('paymentinfo/', views.paymentinfo, name='paymentinfo'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('refund/', views.refund, name='refund'),
    path('rule/', views.rule, name='rule'),
    path('faq/', views.faq, name='faq'),
]