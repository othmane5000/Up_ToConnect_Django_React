from django.urls import path
from . import views

urlpatterns = [
    path('', views.panier_view, name='panier'),
    path('ajouter/<int:product_id>/', views.cart_add, name='cart_add'),
    path('modifier/<int:product_id>/', views.cart_update, name='cart_update'),
    path('supprimer/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('commander/', views.checkout_view, name='checkout'),
    path('confirmation/<int:order_id>/', views.commande_confirmee_view, name='commande_confirmee'),
]