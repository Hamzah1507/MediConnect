from django.contrib import admin
from .models import SignupUser, Medicine, Cart, CheckoutDetails


# ======================================================================
# === CUSTOM ADMIN CLASS WITH FILTER (GUIDELINE #4) ===
# ======================================================================

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for Medicine model with filters
    Satisfies Guideline #4: At least 1 filter on Admin Panel
    """
    # Display these fields in the list view
    list_display = ['name', 'category', 'price', 'id']
    
    # Add filters in the right sidebar
    list_filter = ['category', 'price']  # Filter by category and price
    
    # Add search functionality
    search_fields = ['name', 'description', 'category']
    
    # Fields to display when editing
    fields = ['name', 'description', 'price', 'category', 'image']
    
    # Ordering
    ordering = ['category', 'name']
    
    # Make the list view paginated
    list_per_page = 20


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for Cart model with filters
    """
    list_display = ['user', 'medicine', 'quantity', 'get_total_price']
    list_filter = ['user', 'medicine__category']
    search_fields = ['user__username', 'medicine__name']
    
    def get_total_price(self, obj):
        """Display calculated total price in admin"""
        return f"₹{obj.total_price()}"
    get_total_price.short_description = 'Total Price'


@admin.register(CheckoutDetails)
class CheckoutDetailsAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for CheckoutDetails model
    """
    list_display = ['user', 'prescription_file']
    search_fields = ['user__username']


# Register SignupUser without custom admin (simple registration)
admin.site.register(SignupUser)