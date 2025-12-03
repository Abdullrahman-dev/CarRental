from django.db import models

class Car(models.Model):
    # --- البيانات الأساسية ---
    brand = models.CharField(max_length=50, verbose_name="الشركة المصنعة")
    model_name = models.CharField(max_length=50, verbose_name="الموديل")
    description = models.TextField(verbose_name="الوصف")
    
    # --- المواصفات (التي كانت ناقصة) ---
    TRANSMISSION_CHOICES = [('auto', 'أوتوماتيك'), ('manual', 'عادي')]
    FUEL_CHOICES = [('petrol', 'بنزين'), ('diesel', 'ديزل'), ('hybrid', 'هجين'), ('electric', 'كهرباء')]
    
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='auto', verbose_name="ناقل الحركة")
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, default='petrol', verbose_name="نوع الوقود")
    color = models.CharField(max_length=20, default='أبيض', verbose_name="اللون")
    plate_number = models.CharField(max_length=20, unique=True, default='XXX 0000', verbose_name="رقم اللوحة")
    
    # --- السعر والتوفر ---
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر اليومي")
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="صورة السيارة")
    is_available = models.BooleanField(default=True, verbose_name="متاحة للإيجار؟")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name}"