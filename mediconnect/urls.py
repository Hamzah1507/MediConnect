from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# NOTE: The incorrect line 'from . import views' has been REMOVED. 
# This was the cause of your ImportError.

urlpatterns = [
    # 1. Django Admin Interface
    path('admin/', admin.site.urls),

    # 2. Include ALL URLs from the 'home' app (Your main website logic)
    path('', include('home.urls')), 
    
    # 3. REQUIRED: PayPal IPN URL inclusion (For asynchronous payment confirmation)
    path('paypal/', include('paypal.standard.ipn.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)