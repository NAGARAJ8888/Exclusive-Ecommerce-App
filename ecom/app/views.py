from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, Wishlist, CheckoutItem, Order, OrderItem
from django.http import JsonResponse
from django.contrib import messages
import json

# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product__id', flat=True)

    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        'wishlist_ids': list(wishlist_ids),
    })



@login_required(login_url='login')
def wishlist_view(request):
    products = Product.objects.all()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = [item.product for item in wishlist_items]
    return render(request, 'wishlist.html', {
        'wishlist_products': wishlist_products,
        'products': products,
        
    })


@login_required(login_url='login')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.new_price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


def contact_view(request):
    return render(request, 'contact.html')

def about_view(request):
    return render(request, 'about.html')

def checkout_view(request):
    # Check if already has checkout items
    if not CheckoutItem.objects.filter(user=request.user).exists():
        # Move cart items to checkout
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            CheckoutItem.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity
            )
        cart_items.delete()  # Empty the cart only after copying

    checkout_items = CheckoutItem.objects.filter(user=request.user)
    total = sum(item.product.new_price * item.quantity for item in checkout_items)

    return render(request, 'checkout.html', {
        'cart_items': checkout_items,
        'total': total
    })

@login_required(login_url='login')
def myaccount_view(request):
    return render(request, 'myaccount.html')

def product_view(request):
    return render(request, 'product.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            print("User saved:", user)
            login(request, user)
            return redirect('home')  # or your landing page
        else:
            print(form.errors)
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'reg_form': form})



def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        print("USER: ",user)
        login(request, user)
        return redirect('home')

    return render(request, 'login.html', {'login_form': form})


# views.py
@login_required(login_url='login')
def toggle_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        else:
            return JsonResponse({'status': 'added'})
    
    return JsonResponse({'status': 'error'})


@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, 'Product removed from wishlist.')
    return redirect('wishlist')  # or your wishlist view name


@login_required(login_url='login')
def move_all_to_cart(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)

    for item in wishlist_items:
        # Check if product already in cart
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=item.product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    # Optional: Clear wishlist
    wishlist_items.delete()

    return redirect('wishlist') 

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Cart, id=item_id, user=request.user)
        item.delete()
    return redirect("cart")


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'status': 'success', 'message': 'Product added to cart'})


@login_required(login_url='login')
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            cart_item = Cart.objects.get(id=item_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})


@login_required(login_url='login')
def remove_from_checkout(request, item_id):
    item = get_object_or_404(CheckoutItem, id=item_id, user=request.user)
    item.delete()
    return redirect('checkout')



# views.py
import stripe
from django.conf import settings
from .models import CheckoutItem

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
    checkout_items = CheckoutItem.objects.filter(user=request.user)
    
    if not checkout_items.exists():
        return redirect('checkout')  # prevent empty checkouts

    line_items = []

    for item in checkout_items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.product.title,
                },
                'unit_amount': int(item.product.new_price * 100),  # in paisa
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/order-success/'),
        cancel_url=request.build_absolute_uri('/checkout/'),
    )

    return redirect(session.url, code=303)



@login_required
def order_success(request):
    # Step 1: Get CheckoutItems before deleting them
    items = CheckoutItem.objects.filter(user=request.user)
    
    if not items.exists():
        return redirect('my_orders')  # Already checked out or refreshed

    # Step 2: Create Order
    order = Order.objects.create(user=request.user, is_paid=True)

    # Step 3: Add each item to OrderItem
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    # Step 4: Save items for template before deletion
    purchased_items = list(items)
    items.delete()  # Clear checkout only after recording order

    # Step 5: Render order success page
    return render(request, 'order_success.html', {'purchased_items': purchased_items})



@login_required
def account_profile(request):
    return render(request, 'profile.html')

@login_required
def account_address(request):
    return render(request, 'account_address.html')

@login_required
def account_payment(request):
    return render(request, 'account_payment.html')

@login_required
def my_returns(request):
    return render(request, 'my_returns.html')

@login_required
def my_cancels(request):
    return render(request, 'my_cancels.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_order.html', {'orders': orders})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    context = {
        'product': product,
        'wishlist_ids': wishlist_ids,
    }

    return render(request, 'product.html', context)




def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category__id=category_id)

    # Filter by price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(new_price__gte=min_price)
    if max_price:
        products = products.filter(new_price__lte=max_price)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price or '',
        'max_price': max_price or '',
    }
    return render(request, 'all_products.html', context)


def search_products(request):
    query = request.GET.get('q', '')
    products = []
    if query:
        products = Product.objects.filter(title__icontains=query)[:10]  # limit results
    data = [
        {
            'id': p.id,
            'title': p.title,
            'image': p.image.url if p.image else '',
            'price': p.price
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)