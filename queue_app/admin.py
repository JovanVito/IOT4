from django.contrib import admin
from .models import Antrean

@admin.register(Antrean)
class AntreanAdmin(admin.ModelAdmin):
    # Ini untuk mengatur kolom apa saja yang mau ditampilkan di tabel depan
    list_display = ('nomor_antrean', 'nama', 'nim', 'keperluan', 'status', 'waktu_dibuat')
    
    # BONUS 1: Tambahkan kotak pencarian biar gampang nyari nama/NIM pengunjung
    search_fields = ('nama', 'nim')
    
    # BONUS 2: Tambahkan filter di samping kanan
    list_filter = ('status', 'keperluan', 'waktu_dibuat')
    
    # Biar datanya urut dari yang paling baru
    ordering = ('-waktu_dibuat',)

change_list_template = "antrean_refresh.html"