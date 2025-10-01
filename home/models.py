from django.db import models
from django.contrib.auth.models import User


class SignupUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = "signup_users"
        managed = False


# This is the model for your medicines.
class Medicine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='medicines/')  # 'medicines/' is the folder where images will be saved.
    # Field to store the category
    category = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


# === Cart model ===
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.medicine.name} ({self.quantity})"

    def total_price(self):
        return self.quantity * self.medicine.price

# ==========================================================
# === NEW MODEL: For Prescription Upload (Step 1 of Feature) ===
# ==========================================================
class CheckoutDetails(models.Model):
    """
    Stores temporary checkout information, including the prescription file.
    Uses a OneToOneField to ensure each user only has one active checkout detail record.
    """
    # Links these details uniquely to the user currently checking out
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    # This is the field that saves the path to the uploaded prescription file.
    # Files will be stored in a subfolder named 'prescriptions/' inside your MEDIA_ROOT.
    prescription_file = models.FileField(upload_to='prescriptions/', null=True, blank=True)
    
    def __str__(self):
        return f"Checkout Details for {self.user.username}"