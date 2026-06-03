from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone

# ======== TAMBAHAN: Import PengaturanSistem ========
from .models import Antrean, PengaturanSistem
# ===================================================

@api_view(['POST'])
@permission_classes([AllowAny])

def daftar_antrean_api(request):
    antrean_list = Antrean.objects.filter(status='menunggu').order_by('nomor')[:10] # Ambil 10 teratas
    
    data = []
    for item in antrean_list:
        data.append({
            'nomor': item.nomor,
            'nama': item.nama,
            'keperluan': item.keperluan
        })
    
    return JsonResponse({'daftar': data})

def ambil_antrean(request):
    try:
        hari_ini = timezone.now().date()
        antrean_terakhir = Antrean.objects.filter(waktu_dibuat__date=hari_ini).order_by('-nomor_antrean').first()
        
        nomor_baru = 1 if not antrean_terakhir else antrean_terakhir.nomor_antrean + 1
        
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
        return Response({'error': str(e)}, status=400)


def index_view(request):
    return render(request, 'index.html')

def registrasi_view(request):
    return render(request, 'registrasi.html')

def mobile_view(request):
    return render(request, 'mobile.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def status_antrean(request):
    try:
        antrean_sekarang = Antrean.objects.filter(status='proses').order_by('-waktu_dipanggil').first()
        sisa_menunggu = Antrean.objects.filter(status='menunggu').count()
        
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
        # ================= PERBAIKAN TRIGGER =================
        # 1. Matikan saklar (WAJIB agar Part 1 berhenti bicara)
        setting, created = PengaturanSistem.objects.get_or_create(id=1)
        setting.butuh_dipanggil = False
        setting.save()
        # =====================================================

        # 2. Logika Lama: Cari status 'menunggu', lalu ubah ke 'proses'
        antrean_selanjutnya = Antrean.objects.filter(status='menunggu').order_by('waktu_dibuat').first()
        
        if antrean_selanjutnya:
            antrean_selanjutnya.status = 'proses'
            antrean_selanjutnya.waktu_dipanggil = timezone.now()
            antrean_selanjutnya.save()
            return Response({'message': 'Berhasil', 'nomor_dipanggil': antrean_selanjutnya.nomor_antrean})
        
        return Response({'message': 'Tidak ada antrean yang menunggu'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def selesai_antrean(request):
    antrean = Antrean.objects.filter(status='proses').first()
    if antrean:
        antrean.status = 'selesai'
        antrean.save()
        return Response({'message': f'Antrean {antrean.nomor_antrean} telah selesai'}, status=200)
    return Response({'message': 'Tidak ada antrean yang sedang diproses'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def lewati_antrean(request):
    antrean = Antrean.objects.filter(status='proses').first()
    if antrean:
        antrean.status = 'terlewati'
        antrean.save()
        return Response({'message': f'Antrean {antrean.nomor_antrean} dilewati'}, status=200)
    return Response({'message': 'Tidak ada antrean yang sedang diproses'}, status=400)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def reset_antrean(request):
    Antrean.objects.all().delete()
    return Response({'message': 'Semua antrean berhasil dihapus dan direset ke 0'})


@api_view(['GET'])
@permission_classes([AllowAny])
def daftar_antrean_api(request):
    try:
        antrean_list = Antrean.objects.filter(status='menunggu').order_by('waktu_dibuat')[:10]
        
        data = []
        for item in antrean_list:
            data.append({
                'nomor': item.nomor_antrean,
                'nama': item.nama,
                'keperluan': item.keperluan
            })
        
        return Response({'daftar': data})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


# ================== API BARU: TRIGGER UNTUK ESP32 ==================

@api_view(['POST'])
@permission_classes([AllowAny])
def set_trigger(request):
    """ Ditembak oleh ESP32 Part 2 (Sensor) saat ada orang lewat """
    try:
        setting, created = PengaturanSistem.objects.get_or_create(id=1)
        setting.butuh_dipanggil = True
        setting.save()
        return Response({'message': 'Trigger diset menjadi ON (True)'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def cek_trigger(request):
    """ Di-polling terus menerus oleh ESP32 Part 1 (Audio) """
    try:
        setting, created = PengaturanSistem.objects.get_or_create(id=1)
        
        antrean_selanjutnya = Antrean.objects.filter(status='menunggu').order_by('waktu_dibuat').first()
        
        return Response({
            'butuh_dipanggil': setting.butuh_dipanggil,
            'nomor_dipanggil': antrean_selanjutnya.nomor_antrean if antrean_selanjutnya else 0
        }, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# ===================================================================
