from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model_name', 'description', 'daily_price', 
                  'transmission', 'fuel_type', 'color', 'plate_number', 
                  'image', 'is_available']
        
        # تنسيق الحقول بـ Bootstrap
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: تويوتا'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: كامري'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'daily_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'plate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }