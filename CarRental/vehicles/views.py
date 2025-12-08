from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Car, RentalCompany, CarReview 
from .forms import CarForm, RentalCompanyForm, CarReviewForm 
from django.db.models import Avg, Q 
from django.contrib import messages

# ---------------------------------------------------------
# القسم الأول: واجهة المستخدم (للموقع العام)
# ---------------------------------------------------------

def car_list(request):

    query = request.GET.get('q')
    transmission_filter = request.GET.get('transmission')
    fuel_filter = request.GET.get('fuel')
    
    sort_by = request.GET.get('sort_by')

    cars = Car.objects.all()

    if query:
        cars = cars.filter(
            Q(rental_company__name__icontains=query) | 
            Q(brand__icontains=query) |
            Q(model_name__icontains=query)
        ).distinct()

    if transmission_filter and transmission_filter != 'all':
        cars = cars.filter(transmission=transmission_filter)
        
    if fuel_filter and fuel_filter != 'all':
        cars = cars.filter(fuel_type=fuel_filter)
        
    if sort_by == 'price_asc':

        cars = cars.order_by('daily_price')
    elif sort_by == 'price_desc':

        cars = cars.order_by('-daily_price')

    context = {
        'cars': cars,
        'search_query': query if query else '',

        'selected_transmission': transmission_filter,
        'selected_fuel': fuel_filter,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'fuel_choices': Car.FUEL_CHOICES,

        'selected_sort': sort_by,

        'sort_options': [
            {'value': '', 'label': 'Default'},
            {'value': 'price_asc', 'label': 'Price: Low to High'},
            {'value': 'price_desc', 'label': 'Price: High to Low'},
        ]
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
def edit_company(request, pk):
    company = get_object_or_404(RentalCompany, pk=pk)
    
    if request.method == 'POST':
        form = RentalCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, f'Company "{company.name}" has been updated successfully.')
            return redirect('vehicles:manage_companies')
    else:
        form = RentalCompanyForm(instance=company)
    
    return render(request, 'vehicles/company_form_edit.html', {
        'form': form, 
        'title': f'Edit Company: {company.name}'
    })

@user_passes_test(is_admin)
def delete_company(request, pk):
    company = get_object_or_404(RentalCompany, pk=pk)
    
    car_count = company.cars.count()
    
    if request.method == 'POST':
        company_name = company.name 
        company.delete() 
        
        if car_count > 0:
            messages.success(request, f'Company "{company_name}" and its {car_count} associated cars have been successfully deleted.')
        else:
            messages.success(request, f'Company "{company_name}" has been successfully deleted.')
            
        return redirect('vehicles:manage_companies')
    
    return render(request, 'vehicles/company_confirm_delete.html', {
        'company': company,
        'car_count': car_count,
        'title': f'Confirm Deletion: {company.name}'
    })


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