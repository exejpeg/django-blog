from django.contrib import admin
from .models import Post, Category
from django_mptt_admin.admin import DjangoMpttAdmin

admin.site.register(Post)

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}
