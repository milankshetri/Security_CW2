
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Product import views



urlpatterns = [
    # path('addtocart/<int:p_id>', views.book_details,name='addtocart'),
    path('admin-products', views.admin_products_view,name='admin-products'),
    path('addproduct', views.admin_add_product_view, name='addproduct'),

    path('admin-view-booking', views.admin_view_booking_view, name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view, name='delete-order'),

    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),

    path('cart', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_cart, name="add-to-cart"),
    path('remove_item/<int:cart_item_id>/', views.remove_cart_item, name="remove_item"),

    path('purchaseitem/<int:product_id>/', views.purchaseitem, name="purchaseitem"),
    path('payment', views.payment, name='payment'),

]