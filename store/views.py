from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db import models
from .models import Product, Category
from django.http import JsonResponse


def home(request):
    produits = Product.objects.filter(is_active=True)[:8]

    son_product = Product.objects.filter(
        category='son', is_active=True, image__isnull=False
    ).exclude(image='').first()

    tab_product = Product.objects.filter(
        category='tab', is_active=True, image__isnull=False
    ).exclude(image='').first()

    cam_product = Product.objects.filter(
        category='cam', is_active=True, image__isnull=False
    ).exclude(image='').first()

    return render(request, 'store/home.html', {
        'produits': produits,
        'hero_image': son_product.image.url if son_product and son_product.image else None,
        'son_image': son_product.image.url if son_product and son_product.image else None,
        'tab_image': tab_product.image.url if tab_product and tab_product.image else None,
        'cam_image': cam_product.image.url if cam_product and cam_product.image else None,
    })


CATEGORY_COLORS = {
    'tab': 'blue',
    'vis': 'teal',
    'son': 'purple',
    'res': 'orange',
    'sec': 'red',
    'acc': 'gray',
}

def categorie(request, category_code):
    if category_code not in Category.values:
        raise Http404("Catégorie introuvable")

    produits = Product.objects.filter(category=category_code, is_active=True)
    return render(request, 'store/categorie.html', {
        'produits': produits,
        'categorie_label': dict(Category.choices)[category_code],
        'categorie_color': CATEGORY_COLORS.get(category_code, 'blue'),
    })


def produit_detail(request, slug):
    produit = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/produit_detail.html', {'produit': produit})


def recherche_view(request):
    query = request.GET.get('q', '').strip()

    if query:
        produits = Product.objects.filter(
            is_active=True
        ).filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )
    else:
        produits = Product.objects.none()

    return render(request, 'store/recherche.html', {
        'produits': produits,
        'query': query,
    })

def recherche_live(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'produits': []})

    produits = Product.objects.filter(
        is_active=True
    ).filter(
        models.Q(name__icontains=query) | models.Q(description__icontains=query)
    )[:6]  # on limite à 6 résultats pour rester léger

    data = [
        {
            'name': p.name,
            'price': str(p.price),
            'url': p.get_absolute_url(),
            'image': p.image.url if p.image else '',
        }
        for p in produits
    ]

    return JsonResponse({'produits': data})
