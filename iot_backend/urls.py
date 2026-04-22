from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from LKPS.lkps_project.core import views
from queue_app.views import home, ambil_antrean

# --- TAMBAHAN BARU: Import TemplateView untuk menampilkan HTML ---
from django.views.generic import TemplateView 

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('antrean/', include('antrean.urls')), # Pastikan ini ada
    path('ambil/', views.ambil_antrean, name='ambil'),
    path('panggil/', views.panggil_antrean, name='panggil'),
    path('reset/', views.reset_antrean, name='reset'),
    # Ini untuk mengarahkan ke folder queue_app
    path('api/', include('queue_app.urls')), 
    
    # Ini untuk token JWT kamu
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # =========================================================
    # --- TAMBAHAN BARU: Rute Halaman Frontend (HTML) ---
    # =========================================================
    
    # 1. Halaman Kiosk Registrasi (Muncul saat buka http://127.0.0.1:8000/)
    path('', TemplateView.as_view(template_name='registrasi.html'), name='kiosk_utama'),
    
    # 2. Halaman Meja Admin / TV Loket
    path('admin-loket/', TemplateView.as_view(template_name='index.html'), name='admin_loket'),
    
    # 3. Halaman HP Pengunjung (Nanti diakses via QR Code)
    path('tiket-mobile/', TemplateView.as_view(template_name='mobile.html'), name='tiket_mobile'),
]
