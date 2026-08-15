from django.db import models
from django.urls import reverse


class Category(models.TextChoices):
    TABLEAU = 'tab', 'Tableau interactif & Affichage dynamique'
    VISIOCONFERENCE = 'vis', 'Visioconférence'
    SONORISATION = 'son', 'Sonorisation'
    RESEAUX = 'res', 'Réseaux / VoIP'
    SECURITE = 'sec', 'Sécurité Informatique & Électronique'
    ACCESSOIRES = 'acc', 'Accessoires'


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=3, choices=Category.choices)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('produit_detail', kwargs={'slug': self.slug})