from django.contrib import admin
from django.urls import path
from queue_app import views 

# Import tambahan untuk token JWT (Sesuai dengan kodingan aslimu di halaman kuning)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Rute bawaan Django Admin
    path('admin/', admin.site.urls),

    # ================= RUTE HALAMAN WEB (TAMPILAN UI) =================
    path('', views.index_view, name='index'), 
    path('registrasi/', views.registrasi_view, name='registrasi'), 
    path('tiket-mobile/', views.mobile_view, name='mobile'), 
    
    # Rute ini terlihat di halaman kuningmu sebelumnya, saya kembalikan agar tidak error
    # path('admin-loket/', views.admin_loket_view, name='admin_loket'), 
    # ==================================================================
    # (Di bawah rute-rute antrean milikmu yang sebelumnya)
    path('api/antrean/set_trigger/', views.set_trigger, name='set_trigger'),
    path('api/antrean/cek_trigger/', views.cek_trigger, name='cek_trigger'),


    # ================= RUTE API TOKEN JWT =================
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # ================= RUTE API (UNTUK ESP32 & JAVASCRIPT) =================
    path('api/antrean/ambil/', views.ambil_antrean, name='ambil_antrean'),
    path('api/antrean/status/', views.status_antrean, name='status_antrean'),
    path('api/antrean/panggil/', views.panggil_antrean, name='panggil_antrean'),
    
    path('api/antrean/selesai/', views.selesai_antrean, name='selesai_antrean'),
    path('api/antrean/lewati/', views.lewati_antrean, name='lewati_antrean'),
    path('api/antrean/reset/', views.reset_antrean, name='reset_antrean'), 
    
    # ======== RUTE BARU: UNTUK TABEL DI LAYAR TV ========
    path('api/antrean/daftar/', views.daftar_antrean_api, name='daftar_antrean_api'),
    # =======================================================================
]
