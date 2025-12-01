from django.shortcuts import render, get_object_or_404
from .models import Car

def car_list(request):
    # جلب كلمة البحث من الرابط (إذا وجدت)
    query = request.GET.get('q')
    
    if query:
        # إذا كان هناك بحث، فلتر السيارات حسب الاسم
        cars = Car.objects.filter(name__icontains=query)
    else:
        # وإلا، اعرض كل السيارات
        cars = Car.objects.all()
    
    context = {
        'cars': cars,
        'search_query': query if query else '' # لإبقاء كلمة البحث في المربع
    }
    return render(request, 'vehicles/car_list.html', context)

def car_detail(request, pk):
    # جلب السيارة أو إظهار خطأ 404 إذا لم تكن موجودة
    car = get_object_or_404(Car, pk=pk)
    
    return render(request, 'vehicles/car_detail.html', {'car': car})