from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from vehicles.models import Car 
from decimal import Decimal

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'قيد المراجعة'),
        ('CONFIRMED', 'مؤكد'),
        ('ACTIVE', 'قيد الاستخدام'),
        ('COMPLETED', 'مكتمل'),
        ('CANCELLED', 'ملغي'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name="العميل"
    )
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name="السيارة"
    )

    start_date = models.DateTimeField(verbose_name="تاريخ الاستلام")
    end_date = models.DateTimeField(verbose_name="تاريخ التسليم")
    
    # --- تحديث: دعم الخرائط (إلغاء القائمة المحددة) ---
    pickup_location = models.CharField(
        max_length=255, 
        default='Main Office',
        verbose_name="موقع الاستلام (العنوان)"
    )
    dropoff_location = models.CharField(
        max_length=255, 
        default='Main Office',
        verbose_name="موقع التسليم (العنوان)"
    )

    # حقول جديدة لتخزين الإحداثيات من الخريطة
    pickup_lat = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="خط عرض الاستلام"
    )
    pickup_lng = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="خط طول الاستلام"
    )
    
    dropoff_lat = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="خط عرض التسليم"
    )
    dropoff_lng = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="خط طول التسليم"
    )
    # -----------------------------------------------

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING',
        verbose_name="حالة الحجز"
    )

    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="السعر الإجمالي"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "حجز"
        verbose_name_plural = "الحجوزات"

    def __str__(self):
        return f"Booking #{self.id} - {self.user} - {self.car}"

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("تاريخ التسليم يجب أن يكون بعد تاريخ الاستلام.")
            
            if not self.pk and self.start_date < timezone.now():
                raise ValidationError("لا يمكن الحجز في تاريخ قديم.")

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return max(delta.days, 1)
        return 0

    def save(self, *args, **kwargs):
        # حساب السعر دائماً
        if self.car and self.start_date and self.end_date:
            base_price = self.car.daily_price * self.duration_days
            
            # ميزة One-Way Fee
            # المقارنة الآن تعتمد على اختلاف العنوان النصي
            # (يمكن تطويرها لاحقاً لحساب المسافة بين الإحداثيات بالكيلومتر)
            location_fee = Decimal('0.00')
            if self.pickup_location.lower().strip() != self.dropoff_location.lower().strip():
                location_fee = Decimal('150.00') 

            self.total_price = base_price + location_fee
        
        super().save(*args, **kwargs)