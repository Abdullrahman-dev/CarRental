from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Car
from .forms import CarForm

# ---------------------------------------------------------
# القسم الأول: واجهة المستخدم (للموقع العام)
# ---------------------------------------------------------

def car_list(request):
    # جلب كلمة البحث من الرابط (إذا وجدت)
    query = request.GET.get('q')
    
    if query:
        # البحث في اسم الشركة أو الموديل
        cars = Car.objects.filter(brand__icontains=query) | Car.objects.filter(model_name__icontains=query)
    else:
        # عرض كل السيارات
        cars = Car.objects.all()
    
    context = {
        'cars': cars,
        'search_query': query if query else ''
    }
    return render(request, 'vehicles/car_list.html', context)

def car_detail(request, pk):
    # جلب السيارة أو عرض خطأ 404
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'vehicles/car_detail.html', {'car': car})


# ---------------------------------------------------------
# القسم الثاني: لوحة الإدارة (للأدمن فقط)
# ---------------------------------------------------------

# دالة مساعدة للتحقق: هل المستخدم هو السوبر يوزر (الأدمن)؟
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# 1. لوحة التحكم (عرض جدول السيارات)
@user_passes_test(is_admin)
def manage_cars(request):
    # عرض أحدث السيارات أولاً
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'vehicles/manage_cars.html', {'cars': cars})

# 2. إضافة سيارة جديدة
@user_passes_test(is_admin)
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vehicles:manage_cars')
    else:
        form = CarForm()
    
    return render(request, 'vehicles/car_form.html', {'form': form, 'title': 'إضافة سيارة جديدة'})

# 3. تعديل بيانات سيارة
@user_passes_test(is_admin)
def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('vehicles:manage_cars')
    else:
        form = CarForm(instance=car)
    
    return render(request, 'vehicles/car_form.html', {'form': form, 'title': 'تعديل بيانات السيارة'})

# 4. حذف سيارة
@user_passes_test(is_admin)
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == 'POST':
        car.delete()
        return redirect('vehicles:manage_cars')
    
    return render(request, 'vehicles/confirm_delete.html', {'car': car})