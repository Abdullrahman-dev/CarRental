from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    # الأعمدة المعروضة
    list_display = ('id', 'user', 'car', 'start_date', 'end_date', 'status', 'total_price', 'created_at')
    
    # الفلاتر الجانبية
    list_filter = ('status', 'start_date', 'created_at')
    
    # حقول البحث
    # ⚠️ التعديل المهم هنا:
    # غيرنا car__name (التي لم تعد موجودة) إلى car__brand و car__model_name
    search_fields = ('user__username', 'user__email', 'car__brand', 'car__model_name', 'id')
    
    list_editable = ('status',)
    ordering = ('-created_at',)
    list_per_page = 20

admin.site.register(Booking, BookingAdmin)