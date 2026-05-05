from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem

def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart')


def cart(request):
    items = CartItem.objects.all()
    total = sum(item.total_price() for item in items)
    return render(request, 'shop/cart.html', {'items': items, 'total': total})


def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id)
    item.delete()
    return redirect('cart')


def checkout(request):
    CartItem.objects.all().delete()
    return render(request, 'shop/checkout.html')

# Create your views here.
