from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Produit, Commande
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.safestring import mark_safe

# Create your views here.

# INDEX
@login_required
def index(request):
    orders = Commande.objects.all()
    products = Produit.objects.all()
    workers_count = User.objects.all().count()
    orders_count = orders.count()
    products_count = products.count()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()

    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/index.html', context)

# STAFF
@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Commande.objects.all().count()
    products_count = Produit.objects.all().count()
    context = {
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    workers_count = User.objects.all().count()
    orders_count = Commande.objects.all().count()
    products_count = Produit.objects.all().count()
    context = {
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count
    }
    return render(request, 'dashboard/staff_detail.html', context)


# PRODUIT
@login_required
def product(request):
    items = Produit.objects.all()
    workers_count = User.objects.all().count()
    orders_count = Commande.objects.all().count()
    products_count = items.count()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data.get('nom')
            product_category = form.cleaned_data.get('catégorie')
            product_quantity = form.cleaned_data.get('quantité')
            
            existing_product = Produit.objects.filter(nom=product_name, catégorie=product_category).first()
            if existing_product:
                existing_product.quantité += product_quantity
                existing_product.save()
                if existing_product.quantité <= 20:
                    messages.warning(request, mark_safe(f'La quantité du <strong>{product_name}</strong> a été mise à jour. Stock bas! <strong>{existing_product.quantité}</strong> en stock.'))
                else:
                    messages.success(request, mark_safe(f'La quantié du <strong>{product_name}</strong> a été mise à jour. <strong>{existing_product.quantité}</strong> en stock.'))
            else:
                form.save()
                messages.success(request, mark_safe(f'<strong>{product_name}</strong> a été ajouté.'))
            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form, 
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def product_delete(request, pk):
    item = Produit.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    context = {
        'item': item,
    }
    return render(request, 'dashboard/product_delete.html', context)

@login_required
def product_update(request, pk):
    item = Produit.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/product_update.html', context)


# COMMANDES
@login_required
def order(request):
    orders = Commande.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    products_count = Produit.objects.all().count()

    context = {
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/order.html', context)

@login_required
def respond_to_order(request, order_id):
    try:
        order = Commande.objects.get(id=order_id)
    except Commande.DoesNotExist:
        messages.error(request, "Commande non trouvé.")
        return redirect('dashboard-order')
    
    produit = order.produit

    if request.method == 'POST':
        ordered_quantity = order.commande_quantité
        if ordered_quantity <= produit.quantité:
            produit.quantité -= ordered_quantity
            produit.save()

            order.treated=True
            order.save()

            if(produit.quantité >= 20):
                messages.success(request, mark_safe(f'La commande pour <strong>{order.staff.username}</strong> de <strong>{ordered_quantity} {produit.nom}</strong> a été traité.'))
            else:
                messages.warning(request, mark_safe(f'La commande pour <strong>{order.staff.username}</strong> de <strong>{ordered_quantity} {produit.nom}</strong> a été traité. Il reste que <strong>{produit.quantité}</strong> en stock. Stock bas!'))
            return redirect('dashboard-order')
        else:
            messages.warning(request, mark_safe(f"<strong>{produit.nom}</strong> insuffisant en stock pour effectuer la commande de <strong>{order.staff.username}</strong>."))
            return redirect('dashboard-order')
    
    context = {
        'order': order,
    }
    return render(request, 'dashboard/order.html', context)