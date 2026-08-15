from django.urls import path
from . import views

urlpatterns = [
    path('a-propos/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('blog/', views.blog_list_view, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('politique-de-cookies/', views.cookies_view, name='cookies'),
    path('politique-de-confidentialite/', views.confidentialite_view, name='confidentialite'),
    path('politique-de-retour/', views.retour_view, name='retour'),
]