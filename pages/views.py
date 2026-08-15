from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article
from .forms import ContactForm


def about_view(request):
    return render(request, 'pages/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons rapidement.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'pages/contact.html', {'form': form})


def blog_list_view(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'pages/blog_list.html', {'articles': articles})


def blog_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'pages/blog_detail.html', {'article': article})


def cookies_view(request):
    return render(request, 'pages/cookies.html')


def confidentialite_view(request):
    return render(request, 'pages/confidentialite.html')


def retour_view(request):
    return render(request, 'pages/retour.html')