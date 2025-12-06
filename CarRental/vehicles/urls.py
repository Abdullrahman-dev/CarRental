from django.urls import path
from . import views 
from django.conf import settings

# هذا الاسم مهم جداً لاستخدام Namespaces في القوالب
# مثال: {% url 'vehicles:car_list' %}
app_name = 'vehicles'

urlpatterns = [
    # الرابط الرئيسي للتطبيق: يعرض قائمة السيارات
    # مثال: www.example.com/cars/
    path('', views.car_list, name='car_list'),

    # رابط تفاصيل السيارة: يستقبل رقم السيارة (id)
    # مثال: www.example.com/cars/5/
    path('<int:pk>/', views.car_detail, name='car_detail'),
    path('<int:car_pk>/add-review/', views.add_car_review, name='add_car_review'),

    # --- روابط لوحة الإدارة (للأدمن) ---
    path('manage/', views.manage_cars, name='manage_cars'),
    path('add/', views.add_car, name='add_car'),
    path('edit/<int:pk>/', views.edit_car, name='edit_car'),
    path('delete/<int:pk>/', views.delete_car, name='delete_car'),

    path('companies/manage/', views.manage_companies, name='manage_companies'),
    path('companies/add/', views.add_company, name='add_company'),
]