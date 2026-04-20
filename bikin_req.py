# Script penyelamat untuk memaksa format UTF-8
isi_belanjaan = """asgiref==3.11.1
dj-database-url==3.1.2
Django==5.0.4
django-cors-headers==4.9.0
djangorestframework==3.17.1
djangorestframework_simplejwt==5.3.1
gunicorn==21.2.0
packaging==24.0
PyJWT==2.8.0
sqlparse==0.5.0
tzdata==2024.1
whitenoise==6.6.0
psycopg2-binary==2.9.9
qrcode==7.4.2
Pillow==10.3.0"""

# Membuka file dan memaksa encoding UTF-8
with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(isi_belanjaan)

print("SUKSES! File requirements.txt sekarang sudah 100% bersih dari virus UTF-16 Windows.")