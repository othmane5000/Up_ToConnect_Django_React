from django.contrib import admin
from .models import Article, ContactMessage


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'is_treated', 'created_at')
    list_filter = ('is_treated',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')