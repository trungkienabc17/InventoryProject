from django.contrib import admin
from .models import Produit, Commande

admin.site.site_header = 'Stock Manager Dashboard'

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'catégorie', 'quantité')
    list_filter = ['catégorie']

class CommandeAdmin(admin.ModelAdmin):
    list_display = ('produit', 'commande_quantité', 'staff', 'date')
    list_filter = ['staff', 'produit']

# Register your models here.
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Commande, CommandeAdmin)

