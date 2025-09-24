from django.urls import path
from . import views

urlpatterns = [
    # New entry page, which will be the first page users see.
    path('', views.entry_page, name='entry_page'),

    # This is your main website content, now at a new URL.
    path('home/', views.landing_page, name='home'),

    # Your sign up page remains the same.
    path('signin/', views.signup, name='signin'),

    # We will create a new URL for a dedicated login page.
    path('login/', views.login_view, name='login'),

    # We added this URL for the logout function.
    path('logout/', views.logout_view, name='logout'),

    # The menu page stays the same.
    path('menu/', views.menu, name='menu'),

    # === NEW: URL for search functionality ===
    path('search/', views.search_view, name='search'),

    # === NEW: Cart functionality ===
    path('add-to-cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # === NEW: AJAX URL for minus button ===
    path('remove-from-cart-ajax/<int:medicine_id>/', views.remove_from_cart_ajax, name='remove_from_cart_ajax'),

    # =================================================================
    # === UPDATED: PAYPAL SANDBOX PAYMENT URLS (Replaces Instamojo) ===
    # =================================================================

    # 1. URL to process the payment (Called by the 'Confirm Order' button)
    path('process-payment/<str:total>/', views.process_payment, name='process_payment'),

    # 2. URL for PayPal to redirect to upon SUCCESS.
    path('payment-done/', views.payment_done, name='payment_done'),

    # 3. URL for PayPal to redirect to upon CANCELLATION.
    path('payment-canceled/', views.payment_canceled, name='payment_canceled'),
]