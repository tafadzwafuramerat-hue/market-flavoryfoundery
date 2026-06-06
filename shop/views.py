from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem
import random

def home(request):
    products = Product.objects.all()
    cart_items_count = CartItem.objects.count()
    return render(request, 'shop/home.html', {
        'products': products,
        'items': cart_items_count
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_items_count = CartItem.objects.count()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'items': cart_items_count
    })


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
    cart_items_count = items.count()
    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total,
        'cart_count': cart_items_count
    })


def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id)
    item.delete()
    return redirect('cart')


def checkout(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'Card')
        payment_number = request.POST.get('payment_number', '').strip()
        masked_payment_number = ''
        if payment_number:
            masked_payment_number = '****' + payment_number[-4:]
        order_id = random.randint(10000, 99999)
        CartItem.objects.all().delete()
        return render(request, 'shop/checkout.html', {
            'order_placed': True,
            'payment_method': payment_method,
            'payment_number_display': masked_payment_number,
            'order_id': order_id,
            'estimated_delivery': '15-25 minutes'
        })

    return render(request, 'shop/checkout.html', {
        'order_placed': False,
        'estimated_delivery': '15-25 minutes'
    })

# Create your views here.
