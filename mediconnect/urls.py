from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Django Admin Interface
    path('admin/', admin.site.urls),

    # 2. Include ALL URLs from the 'home' app (Your main website logic)
    path('', include('home.urls')), 
    
    # 3. REQUIRED: PayPal IPN URL inclusion (For asynchronous payment confirmation)
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    # ======================================================================
    # === NEW: REST API ENDPOINTS (GUIDELINE #6) ===
    # ======================================================================
    # API Root: /api/
    # All API endpoints will be available under /api/
    path('api/', include('home.api_urls')),
    
    # Optional: Django REST Framework's browsable API authentication
    # This adds login/logout views for the browsable API interface
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # ======================================================================
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)