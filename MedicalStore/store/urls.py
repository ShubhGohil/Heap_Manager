from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='store-home'),
    path('register/staff', views.staff_register, name='staff-register'),
    path('register/stock', views.stock_register, name='stock-register'),
    path('register/bill', views.bill_register, name='bill-register'),
    path('register/medicine', views.medicine_register, name='medicine-register'),
    path('register/supplier', views.supplier_register, name='supplier-register'),
    path('staff/all/', views.staff_all, name='staff-all'),
    path('staff/delete/<int:pk>', views.staff_delete, name='staff-delete'),
    path('staff/update/<int:pk>', views.staff_update, name='staff-update'),
    path('stock/all/', views.stock_all, name='stock-all'),
    
    
]
