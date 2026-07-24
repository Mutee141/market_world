from django.urls import path
from . import views

app_name = 'storefront'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<str:order_number>/', views.order_success_view, name='order_success'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/login/', views.dashboard_login_view, name='dashboard_login'),
    path('dashboard/stock-adjust/', views.adjust_stock, name='adjust_stock'),
    path('contact/', views.contact_view, name='contact'),
    path('pages/<slug:slug>/', views.cms_page_view, name='cms_page'),
    path('account/', views.customer_account_view, name='account'),
    path('account/orders/<str:order_number>/', views.customer_order_detail_view, name='order_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
