from django import forms
from .models import Booking
from django.db.models import Q

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'start_date', 'end_date', 
            'pickup_location', 'dropoff_location',
            'pickup_lat', 'pickup_lng',
            'dropoff_lat', 'dropoff_lng'
        ]
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            # نجعل حقول العنوان للقراءة فقط لأن الخريطة ستملؤها
            'pickup_location': forms.TextInput(attrs={
                'class': 'form-control bg-light', 
                'placeholder': 'حدد الموقع من الخريطة...',
                'readonly': 'readonly',
                'id': 'id_pickup_location'
            }),
            'dropoff_location': forms.TextInput(attrs={
                'class': 'form-control bg-light', 
                'placeholder': 'حدد الموقع من الخريطة...',
                'readonly': 'readonly',
                'id': 'id_dropoff_location'
            }),
            
            # حقول مخفية لتخزين الإحداثيات بدون أن يراها المستخدم
            'pickup_lat': forms.HiddenInput(attrs={'id': 'id_pickup_lat'}),
            'pickup_lng': forms.HiddenInput(attrs={'id': 'id_pickup_lng'}),
            'dropoff_lat': forms.HiddenInput(attrs={'id': 'id_dropoff_lat'}),
            'dropoff_lng': forms.HiddenInput(attrs={'id': 'id_dropoff_lng'}),
        }

    def __init__(self, *args, **kwargs):
        self.car_id = kwargs.pop('car_id', None) 
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and end <= start:
            raise forms.ValidationError("تاريخ النهاية يجب أن يكون بعد تاريخ البداية.")

        if self.car_id and start and end:
            overlap = Booking.objects.filter(
                car_id=self.car_id,
                status='CONFIRMED'
            ).filter(
                start_date__lt=end,
                end_date__gt=start
            ).exists()

            if overlap:
                raise forms.ValidationError("عذراً، السيارة محجوزة بالفعل في هذه الفترة.")
        
        return cleaned_data