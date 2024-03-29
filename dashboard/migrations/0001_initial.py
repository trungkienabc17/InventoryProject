# Generated by Django 5.0.1 on 2024-01-26 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('catégorie', models.CharField(choices=[('Electroniques', 'Electroniques'), ('Alimentation', 'Alimentation'), ('Papeterie', 'Papeterie')], max_length=20, null=True)),
                ('quantité', models.PositiveBigIntegerField(null=True)),
            ],
        ),
    ]
