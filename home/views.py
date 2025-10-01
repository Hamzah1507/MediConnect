from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.urls import reverse 
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json 
from decimal import Decimal 
import uuid 
from django.core.files.storage import FileSystemStorage 
import os 
from django.contrib.messages import get_messages # <--- NEW IMPORT: Needed to clear old messages

# === NEW IMPORTS for Validation ===
from .utils import validate_prescription_stamp 
# ==================================

# === PAYPAL INTEGRATION IMPORTS ===
from paypal.standard.forms import PayPalPaymentsForm
# ==================================

# NOTE: Assuming models are correctly imported from .models
from .models import SignupUser, Medicine, Cart, CheckoutDetails 

# --- AUTHENTICATION & CORE VIEWS ---

def entry_page(request):
    """Renders the initial page with Log In/Sign Up buttons."""
    return render(request, "entry_page.html")

@login_required
def landing_page(request):
    """Renders the main content page (Home), accessible only when logged in."""
    frequent_medicines = Medicine.objects.all()
    context = {'frequent_medicines': frequent_medicines}
    return render(request, "landing.html", context)

def menu(request):
    return redirect('home')

def signup(request):
    """Handles user registration (Sign Up)."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            messages.success(request, "User registered successfully! Please log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return render(request, "signin.html")

def login_view(request):
    """Handles user login."""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")
    return render(request, "login.html")

def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("entry_page")

def search_view(request):
    """Handles AJAX search functionality."""
    query = request.GET.get('q', '')
    results = []
    if query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )[:5] 
        for medicine in medicines:
            results.append({'name': medicine.name, 'image_url': medicine.image.url if medicine.image else ''})
    return JsonResponse({'results': results})

# --- CART MANAGEMENT VIEWS ---

@login_required
def add_to_cart(request, medicine_id):
    """Adds or increments a medicine item in the user's cart."""
    if request.method == 'POST':
        try:
            medicine = get_object_or_404(Medicine, id=medicine_id)
            
            try:
                # If item exists, increment it
                cart_item = Cart.objects.get(user=request.user, medicine=medicine)
                cart_item.quantity += 1
                message = "Item quantity increased."
            
            except Cart.DoesNotExist:
                # If item does NOT exist, create it with quantity 1
                cart_item = Cart.objects.create(
                    user=request.user,
                    medicine=medicine,
                    quantity=1
                )
                message = "Item added to cart."
            
            cart_item.save()
            
            return JsonResponse({'status': 'success', 'message': message, 'quantity': cart_item.quantity})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def view_cart(request):
    """Renders the cart page, calculating the total."""
    cart_items = Cart.objects.filter(user=request.user)
    # Ensure total is calculated as Decimal
    total = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items, 
        'total': total,
        'total_str': str(total) # Used to pass total via URL parameter
    }
    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, cart_id):
    """Removes a cart item completely (used by the 'Remove' button)."""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def remove_from_cart_ajax(request, medicine_id):
    """Decrements quantity of a cart item (older AJAX view - retained for compatibility)."""
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(Cart, user=request.user, medicine__id=medicine_id)
            
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return JsonResponse({'status': 'success', 'message': 'Item quantity decreased', 'quantity': cart_item.quantity})
            else:
                cart_item.delete()
                return JsonResponse({'status': 'success', 'message': 'Item removed from cart', 'quantity': 0})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
@csrf_exempt
def update_cart_quantity_ajax(request):
    """Handles AJAX requests for incrementing/decrementing quantity from cart buttons (+/-)."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            action = data.get('action')
            
            cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
            
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease':
                cart_item.quantity -= 1
            
            # Save or Delete based on new quantity
            item_was_deleted = False
            if cart_item.quantity > 0:
                cart_item.save()
            else:
                cart_item.delete()
                item_was_deleted = True

            # Recalculate Totals
            new_cart_items = Cart.objects.filter(user=request.user)
            new_grand_total = sum(item.total_price() for item in new_cart_items)
            
            # Prepare the response data safely
            response_data = {
                'status': 'success',
                # Safely return subtotal and quantity
                'subtotal': cart_item.total_price() if not item_was_deleted else 0,
                'quantity': cart_item.quantity if not item_was_deleted else 0,
                'new_grand_total': "%.2f" % new_grand_total # Return total formatted as string
            }
            
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"AJAX Update Error: {str(e)}"}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


# --- PRESCRIPTION UPLOAD & PAYMENT FLOW VIEWS (MODIFIED) ---

@login_required
def checkout_upload(request, total):
    """
    Handles prescription upload, stamp validation, and redirection.
    This is the first step after clicking 'Proceed to Pay' on the cart.
    """
    
    try:
        # Convert total from URL string to Decimal for calculation
        cart_total_decimal = Decimal(total)
        if cart_total_decimal <= 0:
            messages.error(request, "Your cart is empty or total is zero.")
            return redirect('cart')
    except:
        messages.error(request, "Invalid order total provided.")
        return redirect('cart')

    # --- FIX: CLEAR ALL OLD MESSAGES ---
    # This consumes and clears any messages lingering from login/logout/redirects.
    storage = get_messages(request)
    # Simply iterating over the storage object clears the messages from the session
    for message in storage:
        pass 
    # --- END FIX ---

    if request.method == 'POST':
        # NOTE: Ensure the form input name in checkout_upload.html is 'prescription_file'
        uploaded_file = request.FILES.get('prescription_file')

        if uploaded_file:
            # 1. Basic File Type Validation
            valid_types = ['image/jpeg', 'image/png', 'application/pdf']
            if uploaded_file.content_type not in valid_types:
                messages.error(request, "Error: Invalid file type. Please upload a JPEG, PNG, or PDF.")
                return redirect('checkout_upload', total=total)

            # --- START STAMP VALIDATION PROCESS ---
            
            # 2. Save the File Temporarily for Validation
            fs = FileSystemStorage() # Uses settings.MEDIA_ROOT
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_path = os.path.join(settings.MEDIA_ROOT, filename)

            # 3. Perform Stamp Validation
            validation_result = validate_prescription_stamp(uploaded_file_path)

            # 4. Clean up the temporarily saved file (Crucial!)
            fs.delete(filename) 
            
            # 5. Handle Validation Results and Redirection
            if validation_result is True:
                # VALID PRESCRIPTION (STAMP DETECTED or PDF assumed valid)
                
                # Re-save the file PERMANENTLY and update the model
                final_filename = fs.save(uploaded_file.name, uploaded_file) # Re-save the file
                checkout_details, created = CheckoutDetails.objects.get_or_create(user=request.user)
                checkout_details.prescription_file = final_filename
                checkout_details.save()
                
                messages.success(request, "Prescription validated successfully! Redirecting to payment.")
                # Success: Redirect to the final payment view
                return redirect('process_payment', total=total)

            elif validation_result is False:
                # FAKE PRESCRIPTION (NO STAMP DETECTED)
                messages.error(request, "⚠️ **Fake Prescription Alert:** No valid doctor's stamp was detected in the image. Please upload a genuine, stamped prescription.")
                # Redirect back to the upload page with the error
                return redirect('checkout_upload', total=total)

            elif validation_result == "error":
                # IMAGE ERROR (e.g., corrupt file, CV library error)
                messages.error(request, "An error occurred during prescription validation. Please ensure the image is clear and try again.")
                # Redirect back to the upload page with the error
                return redirect('checkout_upload', total=total)

            # --- END STAMP VALIDATION PROCESS ---

        else:
            messages.error(request, "Prescription is required to proceed.")
            # Redirect back to the upload page with the error
            return redirect('checkout_upload', total=total)
            
    context = {
        'grand_total': cart_total_decimal,
        'total_str': total 
    }
    return render(request, 'payment/checkout_upload.html', context)


@login_required
def process_payment(request, total):
    """
    Generates and renders the PayPal payment form.
    NOTE: This view's URL name must be 'process_payment_final' in urls.py.
    """
    from paypal.standard.forms import PayPalPaymentsForm # Imported here for visibility

    try:
        cart_total_decimal = Decimal(total)
    except:
        messages.error(request, "Invalid cart total.")
        return redirect('cart')
    
    if cart_total_decimal <= 0:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    invoice_id = str(uuid.uuid4())
    host = request.get_host()
    
    # NOTE: Currency is forced to USD for reliable Sandbox testing
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL, 
        "amount": f"{cart_total_decimal:.2f}", 
        "currency_code": 'USD',
        
        "item_name": f"MediConnect Order Payment ({request.user.username})",
        "invoice": invoice_id, 
        
        "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return_url": 'http://{}{}'.format(host, reverse('payment_done')),
        "cancel_return": 'http://{}{}'.format(host, reverse('payment_canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    
    return render(request, 'payment/process.html', {'form': form, 'grand_total': cart_total_decimal})


@login_required
def payment_done(request):
    """Redirect target after PayPal payment succeeds (clears cart for demo)."""
    try:
        Cart.objects.filter(user=request.user).delete()
    except Exception:
        pass 

    messages.success(request, "Payment successful! Your order has been placed (Test Mode).")
    return render(request, 'payment/done.html')


@login_required
def payment_canceled(request):
    """Redirect target if user cancels payment."""
    messages.error(request, "Payment was cancelled. Your order has not been placed.")
    return render(request, 'payment/canceled.html')