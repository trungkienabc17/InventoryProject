from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORIE = (
    ('Electroniques', 'Electroniques'),
    ('Alimentation', 'Alimentation'),
    ('Papeterie', 'Papeterie'),
)

class Produit(models.Model):
    nom = models.CharField(max_length=100, null=True)
    catégorie = models.CharField(max_length=20, choices=CATEGORIE, null=True)
    quantité = models.PositiveBigIntegerField(null=True)

    def __str__(self):
        return f'{self.nom}'

class Commande(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    commande_quantité = models.PositiveBigIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True) 
    treated = models.BooleanField(default=False)

    def __str__(self):
        return self.staff.username

