from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.funtest, name='index'),
    path('about/', views.aboutfun, name='about'),
    path('contact/', views.contactfun, name="contact"),
    path('login/', auth_views.LoginView.as_view(template_name= 'registration/login.html')),
    path('home/', views.homefun, name='home'),
]


