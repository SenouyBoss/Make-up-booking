from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView



urlpatterns = [
    path('', views.funtest, name='index'),
    path('about/', views.aboutfun, name='about'),
    path('contact/', views.contactfun, name="contact"),
    #path('login/', auth_views.LoginView.as_view(template_name= 'registration/login.html')),
    #path('home/', views.homefun, name='home'),
    path('home/',  views.home, name='home'),
    path('reg_form/', views.register, name='reg_form'),
    path('login/', views.user_login, name='login2'),
    path('warden_login/', views.warden_login, name='warden_login'),
    path('warden_dues/', views.warden_dues, name='warden_dues'),
    path('warden_add_due/', views.warden_add_due, name='warden_add_due'),
    path('warden_remove_due/', views.warden_remove_due, name='warden_remove_due'),
    path('warden_student_list/', views.warden_student_list, name='warden_student_list'),
    path('warden_student_list/change_student_details/<slug:enrollment_no>', views.change_student_details, name='change_student_details'),
    path('hostels/<slug:hostel_name>/', views.hostel_detail_view, name='hostel'),
    path('login/edit/', views.edit, name='edit'),
    path('login/select/', views.select, name='select'),
    #path('logout/', views.logout_view, name='logout'),
    path('reg_form/login/edit/', views.edit, name='update'),
]




