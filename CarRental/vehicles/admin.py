from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # الأعمدة التي تظهر في القائمة
    list_display = ('brand', 'model_name', 'daily_price', 'is_available', 'created_at')
    
    # فلتر جانبي للبحث السريع (بالشركة وحالة التوفر)
    list_filter = ('brand', 'is_available')
    
    # مربع بحث (باسم الشركة أو الموديل)
    search_fields = ('brand', 'model_name')
    
    # إمكانية تعديل السعر والتوفر مباشرة من القائمة!
    list_editable = ('daily_price', 'is_available')