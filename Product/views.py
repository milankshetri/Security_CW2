from django.shortcuts import render
from itertools import product
from django.shortcuts import redirect, render
from . import forms, models
from .forms import ProductForm
from django.contrib.auth import  authenticate
from django.contrib import messages
# from .models import ProductForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import Cart, CartItem, Product, Orders
from Fulbari.activity_logger import log_activity

# Create your views here.


@login_required(login_url='admin')
def admin_products_view(request):
    products=models.Product.objects.all()

    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    data = {
        'products': paged_product,
    }
    return render(request,'adminControl/admin_product.html',data)

# admin add product by clicking on floating button
@login_required(login_url='admin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'adminControl/addproduct.html',{'productForm':productForm})


@login_required(login_url='admin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


@login_required(login_url='admin')
def update_product_view(request,pk):
    products=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=products)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=products)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'adminControl/admin_update_product.html',{'productForm':productForm,'products':products})


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def cart(request, total=0.0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart, is_active=True)
    except:
        # print("except")
        pass

    context = {
        "cart_items": cart_items,
    }
    return render(request, 'product/cart.html', context)




@login_required(login_url='login')
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    if request.method == "POST":

        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            # messages.success(request, "Item Already In Cart")
            return redirect('product')
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                user=current_user,
            )
            cart_item.save()
            log_activity(current_user, f'added to cart')
            # messages.success(request, "Item Added In Cart")

        return redirect('product')


def remove_cart_item(request, cart_item_id):
    user=request.user
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    messages.success(request, "Item Sucessfully Removed")
    log_activity(user, f'item removed from cart')
    return redirect('product')

def purchaseitem(request, product_id):
    if request.method == "POST":
        current_user = request.user
        product = Product.objects.get(id=product_id)
        
        order = Orders(user=current_user, product=product)
        order.save()

        cart_item_id  = request.POST['cart_item_id']
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()

        messages.success(request, "Item Ordered")
        return redirect('payment')

def payment(request):
    return render(request, 'product/payment.html')

@login_required(login_url='admin')
def admin_view_booking_view(request):
    order = Orders.objects.all()
    paginator = Paginator(order, 2)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    data = {
        'order': paged_product,
    }
    return render(request, 'admincontrol/booking.html', data)

@login_required(login_url='admin')
def delete_order_view(request,pk):
    order=Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')
