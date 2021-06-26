from django.urls import path
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import views as auth_views
from main import views, models, forms

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(form_class=forms.AuthenticationForm,
                                      template_name='login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about-us/', TemplateView.as_view(template_name='about.html'),
         name='about_us'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),
    path('products/<slug:tag>/', views.ProductListView.as_view(), name='products'),
    path('product/<slug:slug>/', DetailView.as_view(model=models.Product), name='product'),
    path('', TemplateView.as_view(template_name='home.html'), name='home')
]
