from django.contrib import admin
from .models import Post, Cart, Item, CartItem


class CartItemAdmin(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
   inlines = [CartItemAdmin,]


admin.site.register(Post)
admin.site.register(Cart, CartAdmin)
admin.site.register(Item)
admin.site.register(CartItem)
