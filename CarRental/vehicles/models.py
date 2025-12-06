from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class RentalCompany(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم شركة التأجير")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "شركة تأجير"
        verbose_name_plural = "شركات التأجير"

class Car(models.Model):

    rental_company = models.ForeignKey(RentalCompany,on_delete=models.CASCADE,related_name='cars',verbose_name="شركة التأجير")

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
    
class CarReview(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="السيارة"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='car_reviews',
        verbose_name="العميل"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم (1-5)"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="التعليق"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('car', 'user') 
        ordering = ['-created_at']
        verbose_name = "تقييم/تعليق سيارة"
        verbose_name_plural = "تقييمات/تعليقات السيارات"