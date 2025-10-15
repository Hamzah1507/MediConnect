"""
REST API Views for MediConnect
Provides API endpoints for accessing and manipulating data
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Medicine, Cart, CheckoutDetails
from .serializers import (
    MedicineSerializer, 
    CartSerializer, 
    CheckoutDetailsSerializer
)


class MedicineViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Medicine model (Primary user-defined model)
    
    Provides CRUD operations:
    - GET /api/medicines/ - List all medicines
    - GET /api/medicines/{id}/ - Retrieve specific medicine
    - POST /api/medicines/ - Create new medicine (admin only)
    - PUT /api/medicines/{id}/ - Update medicine (admin only)
    - DELETE /api/medicines/{id}/ - Delete medicine (admin only)
    
    Additional endpoints:
    - GET /api/medicines/by-category/ - Filter by category
    - GET /api/medicines/search/ - Search medicines
    """
    
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['price', 'name', 'category']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Custom endpoint: Filter medicines by category
        Usage: GET /api/medicines/by-category/?category=Diabetes
        """
        category = request.query_params.get('category', None)
        
        if category:
            medicines = self.queryset.filter(category__iexact=category)
            serializer = self.get_serializer(medicines, many=True)
            return Response({
                'category': category,
                'count': medicines.count(),
                'results': serializer.data
            })
        
        return Response({
            'error': 'Please provide a category parameter'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Custom endpoint: Advanced search for medicines
        Usage: GET /api/medicines/search/?q=glyco
        """
        query = request.query_params.get('q', None)
        
        if query:
            medicines = self.queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
            serializer = self.get_serializer(medicines, many=True)
            return Response({
                'query': query,
                'count': medicines.count(),
                'results': serializer.data
            })
        
        return Response({
            'error': 'Please provide a search query parameter (q)'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """
        Custom endpoint: Get all unique categories
        Usage: GET /api/medicines/categories/
        """
        categories = Medicine.objects.values_list('category', flat=True).distinct()
        categories = [cat for cat in categories if cat]  # Remove None values
        
        return Response({
            'count': len(categories),
            'categories': sorted(categories)
        })
    
    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        """
        Custom endpoint: Get related medicines from same category
        Usage: GET /api/medicines/{id}/related/
        """
        medicine = self.get_object()
        related = Medicine.objects.filter(
            category=medicine.category
        ).exclude(id=medicine.id)[:5]
        
        serializer = self.get_serializer(related, many=True)
        return Response({
            'medicine': medicine.name,
            'category': medicine.category,
            'related_count': related.count(),
            'related_medicines': serializer.data
        })


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Cart operations
    
    Provides:
    - GET /api/cart/ - List user's cart items
    - POST /api/cart/ - Add item to cart
    - PUT /api/cart/{id}/ - Update cart item
    - DELETE /api/cart/{id}/ - Remove from cart
    
    Additional endpoints:
    - GET /api/cart/total/ - Get cart total
    - POST /api/cart/clear/ - Clear entire cart
    """
    
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only the logged-in user's cart items"""
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user when creating a cart item"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def total(self, request):
        """
        Custom endpoint: Get cart total
        Usage: GET /api/cart/total/
        """
        cart_items = self.get_queryset()
        total = sum(item.total_price() for item in cart_items)
        
        return Response({
            'items_count': cart_items.count(),
            'total': float(total),
            'currency': 'INR'
        })
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """
        Custom endpoint: Clear user's entire cart
        Usage: POST /api/cart/clear/
        """
        deleted_count = self.get_queryset().delete()[0]
        
        return Response({
            'message': 'Cart cleared successfully',
            'items_deleted': deleted_count
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def increment(self, request, pk=None):
        """
        Custom endpoint: Increment quantity of cart item
        Usage: POST /api/cart/{id}/increment/
        """
        cart_item = self.get_object()
        cart_item.quantity += 1
        cart_item.save()
        
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def decrement(self, request, pk=None):
        """
        Custom endpoint: Decrement quantity of cart item
        Usage: POST /api/cart/{id}/decrement/
        """
        cart_item = self.get_object()
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data)
        else:
            cart_item.delete()
            return Response({
                'message': 'Item removed from cart (quantity was 1)'
            }, status=status.HTTP_200_OK)


class CheckoutDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Checkout Details
    
    Provides:
    - GET /api/checkout-details/ - Get user's checkout details
    - POST /api/checkout-details/ - Create/upload prescription
    - PUT /api/checkout-details/{id}/ - Update prescription
    """
    
    serializer_class = CheckoutDetailsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only the logged-in user's checkout details"""
        return CheckoutDetails.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user when creating checkout details"""
        serializer.save(user=self.request.user)
