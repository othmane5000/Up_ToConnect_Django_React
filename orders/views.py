from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings


def panier_view(request):
    cart = Cart(request)
    return render(request, 'orders/panier.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1
    success = cart.add(product_id, quantity)
    if success:
        messages.success(request, "Produit ajouté au panier.")
    else:
        messages.error(request, "Ce produit n'est pas disponible.")
    return redirect('panier')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(product_id, quantity)
    return redirect('panier')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('panier')


@login_required(login_url='login')
def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Votre panier est vide.")
        return redirect('panier')

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, status='PENDING')
        for item in cart:
            product = item['product']
            if item['quantity'] > product.stock:
                messages.error(request, f"Stock insuffisant pour {product.name}.")
                order.delete()
                return redirect('panier')

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                unit_price=product.price
            )
            product.stock -= item['quantity']
            product.save()

        cart.clear()

        items_list = "\n".join([
            f"- {item.product.name} x{item.quantity} = {item.subtotal} MAD"
            for item in order.items.all()
        ])

        # ===== EMAIL 1 : NOTIFICATION VERS L'ENTREPRISE =====
        admin_email_body = f"""
Nouvelle commande reçue sur UpToConnect !

Commande #{order.id}
Client : {request.user.username} ({request.user.email})

Produits commandés :
{items_list}

Total : {order.total} MAD

Connectez-vous à l'admin pour traiter cette commande :
http://127.0.0.1:8000/admin/orders/order/{order.id}/change/
        """

        try:
            send_mail(
                subject=f"Nouvelle commande #{order.id} - UpToConnect",
                message=admin_email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        # ===== EMAIL 2 : CONFIRMATION VERS LE CLIENT =====
        client_email_body = f"""
Bonjour {request.user.first_name or request.user.username},

Merci pour votre commande sur UpToConnect !

Récapitulatif de votre commande #{order.id} :

{items_list}

Total payé : {order.total} MAD
Statut : En attente de traitement

Notre équipe va traiter votre commande dans les plus brefs délais et vous contactera pour organiser la livraison.

Pour toute question, n'hésitez pas à nous contacter :
- Téléphone : +212 6 69 272 386
- Email : contact@uptoconnect.com

Merci de votre confiance,
L'équipe UpToConnect
        """

        try:
            if request.user.email:
                send_mail(
                    subject=f"Confirmation de votre commande #{order.id} - UpToConnect",
                    message=client_email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
        except Exception:
            pass

        messages.success(request, "Votre commande a été enregistrée avec succès !")
        return redirect('commande_confirmee', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required(login_url='login')
def commande_confirmee_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/commande_confirmee.html', {'order': order})