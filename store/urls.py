from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recherche/', views.recherche_view, name='recherche'),
    path('categorie/<str:category_code>/', views.categorie, name='categorie'),
    path('recherche-live/', views.recherche_live, name='recherche_live'),
    path('produit/<slug:slug>/', views.produit_detail, name='produit_detail'),
]