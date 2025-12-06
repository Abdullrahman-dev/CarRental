from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.auth_page, name='auth_page'),
    path('contact/', views.contact, name='contact'),
    path('about-us/', views.about_us, name='about_us'),
    path('careers/', views.careers, name='careers'),
    path('dashboard/messages/', views.contact_messages_dashboard, name='contact_messages_dashboard'),
]