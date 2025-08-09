from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),  # ✅ FIXED LINE
    path('login/', views.login_view, name='login'),  # ✅ FIXED LINE
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('myaccount/', views.myaccount_view, name='myaccount'),
    path('product/', views.product_view, name='product'),
    path('logout/', views.logout_view, name='logout'),
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/move_all_to_cart/', views.move_all_to_cart, name='move_all_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-checkout/<int:item_id>/', views.remove_from_checkout, name='remove_from_checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('order-success/', views.order_success, name='order_success'),
    path('account/', views.account_profile, name='account_profile'),
    path('account/address/', views.account_address, name='account_address'),
    path('account/payment/', views.account_payment, name='account_payment'),
    path('account/return/', views.my_returns, name='my_returns'),
    path('account/cancel/', views.my_cancels, name='my_cancels'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/', views.all_products, name='all_products'),
    path('search/', views.search_products, name='search'),
]
