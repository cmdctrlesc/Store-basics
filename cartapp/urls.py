
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:record_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:record_id>/', views.cart_remove, name='cart_remove'),
]

# url(r'^remove/(?P<record_id>\d+)/$', views.cart_remove, name='cart_remove'),
