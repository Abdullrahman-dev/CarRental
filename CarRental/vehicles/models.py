from django.db import models

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('auto', 'أوتوماتيك'),
        ('manual', 'عادي'),
    ]
    
    FUEL_CHOICES = [
        ('petrol', 'بنزين'),
        ('diesel', 'ديزل'),
        ('hybrid', 'هجين'),
        ('electric', 'كهرباء'),
    ]

    name = models.CharField(max_length=100, verbose_name="اسم السيارة")
    model_year = models.IntegerField(verbose_name="الموديل")
    plate_number = models.CharField(max_length=20, unique=True, verbose_name="رقم اللوحة")
    color = models.CharField(max_length=20, verbose_name="اللون")
    
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='auto', verbose_name="ناقل الحركة")
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, default='petrol', verbose_name="نوع الوقود")
    
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر اليومي")
    # تأكدنا من جعل الصورة اختيارية (blank=True) لتجنب الأخطاء إذا لم ترفع صورة
    image = models.ImageField(upload_to='cars/', verbose_name="صورة السيارة", blank=True, null=True)
    
    is_available = models.BooleanField(default=True, verbose_name="متاحة للإيجار؟")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.model_year})"