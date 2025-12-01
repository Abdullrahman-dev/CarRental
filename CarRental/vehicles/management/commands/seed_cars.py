from django.core.management.base import BaseCommand
from vehicles.models import Car
import random

class Command(BaseCommand):
    help = 'تعبئة قاعدة البيانات ببيانات سيارات وهمية للتجربة'

    def handle(self, *args, **kwargs):
        # قائمة بسيارات متنوعة لإضافتها
        cars_data = [
            {
                "name": "تويوتا كامري",
                "model_year": 2023,
                "plate_number": "ABC 1234",
                "color": "أبيض لؤلؤي",
                "daily_price": 200,
                "transmission": "auto",
                "fuel_type": "petrol",
            },
            {
                "name": "هيونداي أكسنت",
                "model_year": 2022,
                "plate_number": "KSA 5555",
                "color": "فضي",
                "daily_price": 120,
                "transmission": "auto",
                "fuel_type": "petrol",
            },
            {
                "name": "فورد تورس",
                "model_year": 2024,
                "plate_number": "XYZ 9876",
                "color": "أسود ملكي",
                "daily_price": 350,
                "transmission": "auto",
                "fuel_type": "petrol",
            },
            {
                "name": "لوسيد آير",
                "model_year": 2025,
                "plate_number": "ELEC 2030",
                "color": "ذهبي",
                "daily_price": 1500,
                "transmission": "auto",
                "fuel_type": "electric",
            },
            {
                "name": "جمس يوكن",
                "model_year": 2021,
                "plate_number": "GMC 1000",
                "color": "كحلي",
                "daily_price": 600,
                "transmission": "auto",
                "fuel_type": "petrol",
            },
            {
                "name": "تويوتا هايلكس",
                "model_year": 2023,
                "plate_number": "HLX 4444",
                "color": "أبيض",
                "daily_price": 250,
                "transmission": "manual",
                "fuel_type": "diesel",
            },
        ]

        self.stdout.write(self.style.WARNING('جاري إضافة السيارات...'))

        for data in cars_data:
            # نستخدم get_or_create لتجنب تكرار البيانات إذا شغلت الأمر مرتين
            car, created = Car.objects.get_or_create(
                plate_number=data['plate_number'],
                defaults=data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ تمت إضافة: {car.name}'))
            else:
                self.stdout.write(f'⚠️ موجودة مسبقاً: {car.name}')

        self.stdout.write(self.style.SUCCESS('\nتم الانتهاء بنجاح! قاعدة البيانات جاهزة الآن.'))