"""
REST API Serializers for MediConnect Models
These serializers convert Django models to JSON format for the REST API
"""

from rest_framework import serializers
from .models import Medicine, Cart, CheckoutDetails
from django.contrib.auth.models import User


class MedicineSerializer(serializers.ModelSerializer):
    """
    Serializer for Medicine model - Primary user-defined model
    Converts Medicine objects to JSON and validates incoming data
    """
    
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'description', 'price', 'image', 'category']
        read_only_fields = ['id']
    
    def validate_price(self, value):
        """Custom validation: Price must be positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_name(self, value):
        """Custom validation: Name must not be empty"""
        if not value or value.strip() == "":
            raise serializers.ValidationError("Medicine name cannot be empty.")
        return value


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model with nested medicine details
    """
    medicine = MedicineSerializer(read_only=True)
    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(),
        source='medicine',
        write_only=True
    )
    total_price = serializers.SerializerMethodField()
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user_username', 'medicine', 'medicine_id', 'quantity', 'total_price']
        read_only_fields = ['id', 'total_price']
    
    def get_total_price(self, obj):
        """Calculate total price for the cart item"""
        return obj.total_price()
    
    def validate_quantity(self, value):
        """Custom validation: Quantity must be positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Simple User serializer for user information in responses
    """
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CheckoutDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for CheckoutDetails model
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CheckoutDetails
        fields = ['user', 'user_username', 'prescription_file']