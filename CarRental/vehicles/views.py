from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Car, RentalCompany, CarReview 
from .forms import CarForm, RentalCompanyForm, CarReviewForm 
from django.db.models import Avg

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
    car = get_object_or_404(Car, pk=pk)
    
    # حساب متوسط التقييمات
    average_rating = car.reviews.aggregate(Avg('rating'))['rating__avg']
    
    # جلب جميع التعليقات
    reviews = CarReview.objects.filter(car=car).order_by('-created_at')

    review_form = CarReviewForm()
    
    # التحقق مما إذا كان المستخدم يستطيع إضافة تقييم (لم يقيّم من قبل)
    user_can_review = request.user.is_authenticated and not CarReview.objects.filter(car=car, user=request.user).exists()
    
    context = {
        'car': car,
        'average_rating': round(average_rating, 1) if average_rating else 0, # تقريب لرقم عشري واحد
        'reviews': reviews,
        'review_form': review_form,
        'user_can_review': user_can_review,
    }
    return render(request, 'vehicles/car_detail.html', context)

@login_required
def add_car_review(request, car_pk):
    car = get_object_or_404(Car, pk=car_pk)
    
    # منع التقييم المكرر
    if CarReview.objects.filter(car=car, user=request.user).exists():
        # يمكنك عرض رسالة خطأ هنا
        return redirect('vehicles:car_detail', pk=car_pk)
        
    if request.method == 'POST':
        form = CarReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            return redirect('vehicles:car_detail', pk=car_pk)
    
    return redirect('vehicles:car_detail', pk=car_pk)


# ---------------------------------------------------------
# القسم الثاني: لوحة الإدارة (للأدمن فقط)
# ---------------------------------------------------------


# دالة مساعدة للتحقق: هل المستخدم هو السوبر يوزر (الأدمن)؟
def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin)
def manage_companies(request):
    companies = RentalCompany.objects.all().order_by('name')
    context = {
        'companies': companies,
        'title': 'إدارة شركات التأجير'
    }
    return render(request, 'vehicles/manage_companies.html', context)

@user_passes_test(is_admin)
def add_company(request):
    if request.method == 'POST':
        form = RentalCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicles:manage_companies') 
    else:
        form = RentalCompanyForm()
    
    return render(request, 'vehicles/company_form.html', {'form': form, 'title': 'إضافة شركة تأجير جديدة'})

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