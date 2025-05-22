from django.contrib import admin
from .models import Product, ProductImage, Feedback

# Inline for adding multiple images within Product admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Show 1 empty row by default
    fields = ('image', 'title')  # Fields to show in inline

# Customize Product admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')  # Columns in list view
    search_fields = ('name', 'category')          # Search bar
    list_filter = ('category',)                   # Sidebar filter
    inlines = [ProductImageInline]                # Add ProductImage inline

# Customize Feedback admin
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'rating', 'created_at')
    search_fields = ('name', 'email', 'comment')
    list_filter = ('rating', 'created_at')

# Register models with admin
admin.site.register(Product, ProductAdmin)
admin.site.register(Feedback, FeedbackAdmin)
