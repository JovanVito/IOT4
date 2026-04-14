from django.db import models

class Antrean(models.Model):
    STATUS_CHOICES = (
        ('MENUNGGU', 'Menunggu'),
        ('DIPANGGIL', 'Dipanggil'),
        ('SELESAI', 'Selesai'),
    )
    
    nomor_antrean = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='MENUNGGU')
    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    waktu_dipanggil = models.DateTimeField(null=True, blank=True)

    # --- TAMBAHAN 3 KOLOM BARU UNTUK DATA PENGUNJUNG ---
    nama = models.CharField(max_length=100, null=True, blank=True)
    nim = models.CharField(max_length=50, null=True, blank=True)
    keperluan = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        # Biar di panel admin kelihatan keren: "Antrean 1 - Budi Santoso (Menunggu)"
        nama_tampil = self.nama if self.nama else 'Anonim'
        return f"Antrean {self.nomor_antrean} - {nama_tampil} ({self.status})"