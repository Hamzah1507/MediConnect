"""
REST API URL Configuration for MediConnect
Defines all API endpoints using Django REST Framework's router
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import MedicineViewSet, CartViewSet, CheckoutDetailsViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()

# Register viewsets - these create all standard CRUD endpoints automatically
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'checkout-details', CheckoutDetailsViewSet, basename='checkout-details')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

"""
Available API Endpoints:

MEDICINES (Primary User-Defined Model):
    GET     /api/medicines/                     - List all medicines
    POST    /api/medicines/                     - Create new medicine
    GET     /api/medicines/{id}/                - Get specific medicine
    PUT     /api/medicines/{id}/                - Update medicine
    DELETE  /api/medicines/{id}/                - Delete medicine
    GET     /api/medicines/by-category/         - Filter by category (Custom)
    GET     /api/medicines/search/              - Search medicines (Custom)
    GET     /api/medicines/categories/          - List all categories (Custom)
    GET     /api/medicines/{id}/related/        - Get related medicines (Custom)

CART:
    GET     /api/cart/                          - List cart items
    POST    /api/cart/                          - Add to cart
    GET     /api/cart/{id}/                     - Get cart item
    PUT     /api/cart/{id}/                     - Update cart item
    DELETE  /api/cart/{id}/                     - Remove from cart
    GET     /api/cart/total/                    - Get cart total (Custom)
    POST    /api/cart/clear/                    - Clear cart (Custom)
    POST    /api/cart/{id}/increment/           - Increment quantity (Custom)
    POST    /api/cart/{id}/decrement/           - Decrement quantity (Custom)

CHECKOUT DETAILS:
    GET     /api/checkout-details/              - List checkout details
    POST    /api/checkout-details/              - Create/upload prescription
    GET     /api/checkout-details/{id}/         - Get checkout details
    PUT     /api/checkout-details/{id}/         - Update prescription

Authentication required for most endpoints (except reading medicines)
"""