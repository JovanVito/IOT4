from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.http import HttpResponse # <--- TAMBAHAN UNTUK FAVICON

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from LKPS.lkps_project.core import views
from queue_app.views import home, ambil_antrean

# --- FUNGSI PENANGKAL ERROR FAVICON VERCEL ---
def dummy_favicon(request):
    return HttpResponse(status=204)


urlpatterns = [
    # =========================================================
    # 1. HALAMAN FRONTEND (TAMPILAN UI)
    # =========================================================
    
    # Halaman Kiosk Registrasi (Muncul saat pertama kali buka website)
    # Catatan: path('', home) saya hapus agar tidak menutupi rute ini.
    path('', TemplateView.as_view(template_name='registrasi.html'), name='kiosk_utama'),
    
    # Halaman Meja Admin / TV Loket
    path('admin-loket/', TemplateView.as_view(template_name='index.html'), name='admin_loket'),
    
    # Halaman HP Pengunjung (Nanti diakses via QR Code)
    path('tiket-mobile/', TemplateView.as_view(template_name='mobile.html'), name='tiket_mobile'),


    # =========================================================
    # 2. RUTE BACKEND & API (LOGIKA DATA)
    # =========================================================
    
    path('admin/', admin.site.urls),
    
    # Mengarahkan ke file urls.py di dalam masing-masing folder app
    path('antrean/', include('antrean.urls')), 
    path('api/', include('queue_app.urls')), 
    
    # Rute aksi manual (tanpa /api/)
    path('ambil/', views.ambil_antrean, name='ambil'),
    path('panggil/', views.panggil_antrean, name='panggil'),
    path('reset/', views.reset_antrean, name='reset'),
    
    # Rute Token JWT untuk Autentikasi Keamanan
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # =========================================================
    # 3. PELINDUNG SISTEM
    # =========================================================
    path('favicon.ico', dummy_favicon), # <--- MENCEGAH ERROR 500 DI VERCEL
]
