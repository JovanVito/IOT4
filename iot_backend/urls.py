from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.http import HttpResponse

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# --- Panggil fungsi HANYA dari queue_app ---
from queue_app import views as queue_views 

def dummy_favicon(request):
    return HttpResponse(status=204)

urlpatterns = [
    # =========================================================
    # 1. HALAMAN FRONTEND (TAMPILAN UI)
    # =========================================================
    path('', TemplateView.as_view(template_name='registrasi.html'), name='kiosk_utama'),
    path('admin-loket/', TemplateView.as_view(template_name='index.html'), name='admin_loket'),
    path('tiket-mobile/', TemplateView.as_view(template_name='mobile.html'), name='tiket_mobile'),

    # =========================================================
    # 2. RUTE BACKEND & KEAMANAN JWT
    # =========================================================
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # =========================================================
    # 3. RUTE API ANTREAN (UNTUK ESP32 & FRONTEND)
    # =========================================================
    path('api/antrean/ambil/', queue_views.ambil_antrean, name='ambil'),
    path('api/antrean/status/', queue_views.status_antrean, name='status'),
    path('api/antrean/panggil/', queue_views.panggil_antrean, name='panggil'),
    path('api/antrean/reset/', queue_views.reset_antrean, name='reset'),

    # =========================================================
    # 4. PELINDUNG SISTEM VERCEL
    # =========================================================
    path('favicon.ico', dummy_favicon),
]
