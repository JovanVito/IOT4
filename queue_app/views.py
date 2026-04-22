from django.shortcuts import render # <--- TAMBAHAN WAJIB AGAR TIDAK ERROR 500 DI HALAMAN DEPAN
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Antrean

@api_view(['POST'])
@permission_classes([AllowAny])
def ambil_antrean(request):
    try:
        hari_ini = timezone.now().date()
        antrean_terakhir = Antrean.objects.filter(waktu_dibuat__date=hari_ini).order_by('-nomor_antrean').first()
        
        nomor_baru = 1 if not antrean_terakhir else antrean_terakhir.nomor_antrean + 1
        
        # DRF otomatis parsing JSON, asalkan ESP32 pakai header Content-Type: application/json
        nama_pengunjung = request.data.get('nama', 'Anonim Walk-in')
        nim_pengunjung = request.data.get('nim', '-')
        keperluan_pengunjung = request.data.get('keperluan', 'Ambil via Sensor')

        antrean = Antrean.objects.create(
            nomor_antrean=nomor_baru,
            nama=nama_pengunjung,
            nim=nim_pengunjung,
            keperluan=keperluan_pengunjung
        )
        
        return Response({'message': 'Antrean berhasil diambil', 'nomor': antrean.nomor_antrean}, status=201)
    
    except Exception as e:
        # JIKA TERJADI ERROR, VERCEL TIDAK AKAN 500, TAPI MENGELUARKAN PESAN ERRORNYA!
        return Response({'error': str(e)}, status=400)


def home(request):
    return render(request, 'index.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def status_antrean(request):
    try:
        antrean_sekarang = Antrean.objects.filter(status='DIPANGGIL').order_by('-waktu_dipanggil').first()
        sisa_menunggu = Antrean.objects.filter(status='MENUNGGU').count()
        
        return Response({
            'antrean_sekarang': antrean_sekarang.nomor_antrean if antrean_sekarang else 0,
            'sisa_menunggu': sisa_menunggu
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def panggil_antrean(request):
    try:
        antrean_selanjutnya = Antrean.objects.filter(status='MENUNGGU').order_by('waktu_dibuat').first()
        
        if antrean_selanjutnya:
            antrean_selanjutnya.status = 'DIPANGGIL'
            antrean_selanjutnya.waktu_dipanggil = timezone.now()
            antrean_selanjutnya.save()
            return Response({'message': 'Berhasil', 'nomor_dipanggil': antrean_selanjutnya.nomor_antrean})
        
        return Response({'message': 'Tidak ada antrean yang menunggu'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def reset_antrean(request):
    Antrean.objects.all().delete()
    return Response({'message': 'Semua antrean berhasil dihapus dan direset ke 0'})
