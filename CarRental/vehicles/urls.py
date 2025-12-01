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

]