from django import forms
from .models import Produit, Commande

class ProductForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'catégorie', 'quantité']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['produit', 'commande_quantité']