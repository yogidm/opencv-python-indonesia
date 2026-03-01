# 08 Frequency Domain dan Transformasi Fourier

---

## 1. Pendahuluan Teoretis

Pada domain spasial, citra direpresentasikan sebagai fungsi diskret dua dimensi:

$$
f(x,y), \quad x = 0,1,\dots,M-1,\quad y = 0,1,\dots,N-1
$$

dengan:

- $f(x,y)$ adalah intensitas piksel pada koordinat $(x,y)$  
- $M, N$ adalah dimensi citra  

Representasi ini bersifat lokal. Setiap operasi spasial memodifikasi piksel berdasarkan lingkungan sekitarnya. Namun banyak fenomena fisik dan gangguan sistem (misalnya interferensi elektromagnetik, vibrasi periodik, atau pola tekstur terstruktur) lebih mudah dianalisis pada domain frekuensi.

Transformasi Fourier Diskret dua dimensi (2D-DFT) didefinisikan sebagai:

$$
F(u,v) = \sum_{x=0}^{M-1}\sum_{y=0}^{N-1} 
f(x,y)\, e^{-j2\pi\left(\frac{ux}{M} + \frac{vy}{N}\right)}
$$

dengan:

- $F(u,v)$ adalah representasi spektral
- $u, v$ indeks frekuensi horizontal dan vertikal
- $j = \sqrt{-1}$ unit imajiner

Inverse transform:

$$
f(x,y) = \frac{1}{MN} 
\sum_{u=0}^{M-1}\sum_{v=0}^{N-1} 
F(u,v)\, e^{j2\pi\left(\frac{ux}{M} + \frac{vy}{N}\right)}
$$

### Interpretasi Matematis

DFT mendekomposisi citra menjadi superposisi fungsi basis sinusoidal kompleks. Setiap pasangan $(u,v)$ merepresentasikan frekuensi spasial tertentu.

### Interpretasi Engineering

- Frekuensi rendah → struktur global (latar, iluminasi)
- Frekuensi tinggi → tepi, noise, detail halus
- Noise periodik → spike spesifik pada spektrum

Domain frekuensi memungkinkan pemisahan komponen tersebut secara eksplisit.

---

## 2. Magnitude Spectrum dan Representasi Energi

Spektrum magnitudo:

$$
|F(u,v)| = \sqrt{ \Re(F)^2 + \Im(F)^2 }
$$

Untuk visualisasi:

$$
S(u,v) = \log\left(1 + |F(u,v)|\right)
$$

Transformasi log digunakan karena rentang dinamis spektrum sangat besar.

Secara statistik, energi citra dalam domain frekuensi memenuhi Teorema Parseval:

$$
\sum_{x,y} |f(x,y)|^2 = \frac{1}{MN}\sum_{u,v} |F(u,v)|^2
$$

Ini menyatakan konservasi energi.

---

## 3. Teorema Konvolusi dan Kompleksitas

Jika:

$$
g(x,y) = f(x,y) * h(x,y)
$$

maka:

$$
G(u,v) = F(u,v)\cdot H(u,v)
$$

Kompleksitas:

- Konvolusi spasial: $O(MNk^2)$
- FFT: $O(MN \log(MN))$

Untuk kernel besar, FFT lebih efisien.

---

## 4. Implementasi OpenCV DFT

Struktur fungsi:

```
cv2.dft(src, flags=cv2.DFT_COMPLEX_OUTPUT)
```

Parameter penting:

- `src` : citra float32
- `DFT_COMPLEX_OUTPUT` : output 2-channel (real, imag)
- `DFT_INVERSE`
- `DFT_SCALE`

---

# 5. Studi Kasus 1 — Penghilangan Noise Periodik pada Sistem Industri

## Permasalahan Lapangan

Pada lini produksi berbasis conveyor, kamera vision system mengalami interferensi elektromagnetik yang menghasilkan pola garis periodik horizontal.

Noise ini bersifat sinusoidal → muncul sebagai spike simetris pada domain frekuensi.

## Pipeline

1. FFT
2. Identifikasi spike frekuensi
3. Desain notch filter
4. Inverse FFT
5. Evaluasi struktur kontur

---

## Implementasi Lengkap

```python
import cv2
import numpy as np

# Membaca citra grayscale
img = cv2.imread('noisy_image.jpg', 0)

# Konversi ke float32
img_float = np.float32(img)

# DFT
dft = cv2.dft(img_float, flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

# Magnitude spectrum untuk visualisasi
magnitude = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])
spectrum = np.log(1 + magnitude)

# Membuat notch filter manual
rows, cols = img.shape
mask = np.ones((rows, cols, 2), np.uint8)

crow, ccol = rows//2 , cols//2

# Titik noise (contoh estimasi manual)
notch_radius = 10
noise_points = [(crow+40, ccol), (crow-40, ccol)]

for point in noise_points:
    r, c = point
    for i in range(rows):
        for j in range(cols):
            if np.sqrt((i-r)**2 + (j-c)**2) <= notch_radius:
                mask[i,j] = 0

# Aplikasikan mask
fshift = dft_shift * mask

# Inverse FFT
f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])

# Normalisasi
img_back_norm = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX)
img_back_uint8 = np.uint8(img_back_norm)

# Visualisasi
comparison = np.hstack((img, img_back_uint8))

cv2.imshow('Original vs Notch Filtered', comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Analisis Engineering

Jika radius notch terlalu besar:

- Detail frekuensi valid ikut terhapus
- Kontur menjadi kehilangan ketajaman

Jika terlalu kecil:

- Noise residual masih muncul

Trade-off harus mempertimbangkan pipeline lanjutan seperti contour detection atau feature extraction.

---

# 6. Studi Kasus 2 — Peningkatan Ketajaman Dokumen untuk OCR

## Permasalahan

Dokumen hasil scan buram (defocus ringan), menyebabkan OCR gagal mengenali huruf tipis.

## Strategi

High-pass filter pada domain frekuensi untuk menonjolkan komponen frekuensi tinggi.

---

## Implementasi

```python
import cv2
import numpy as np

img = cv2.imread('document.jpg', 0)
img_float = np.float32(img)

rows, cols = img.shape

dft = cv2.dft(img_float, flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

# High-pass mask
mask = np.ones((rows, cols, 2), np.uint8)
crow, ccol = rows//2 , cols//2
radius = 30

for i in range(rows):
    for j in range(cols):
        if np.sqrt((i-crow)**2 + (j-ccol)**2) <= radius:
            mask[i,j] = 0

fshift = dft_shift * mask

f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])

img_back_norm = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX)
img_back_uint8 = np.uint8(img_back_norm)

comparison = np.hstack((img, img_back_uint8))

cv2.imshow('Original vs High Pass', comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Analisis Engineering

Radius kecil:

- Edge tajam
- Noise meningkat
- Fragmentasi huruf

Radius besar:

- Edge kurang signifikan
- OCR tetap gagal

High-pass ekstrem dapat mengubah topologi huruf (lubang pada huruf “O” bisa hilang).

---

# 7. Studi Kasus 3 — Deteksi Pola Getaran pada Struktur (Structural Monitoring)

## Permasalahan

Dalam eksperimen shaking table, kamera merekam pola retakan mikro yang dipengaruhi getaran periodik.

Tujuan: mendeteksi frekuensi dominan dari pola citra.

---

## Implementasi Spektrum Analisis

```python
import cv2
import numpy as np

img = cv2.imread('structure.jpg', 0)
img_float = np.float32(img)

dft = cv2.dft(img_float, flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

magnitude = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])
spectrum = np.log(1 + magnitude)

spectrum_norm = cv2.normalize(spectrum, None, 0, 255, cv2.NORM_MINMAX)
spectrum_uint8 = np.uint8(spectrum_norm)

comparison = np.hstack((img, spectrum_uint8))

cv2.imshow('Structure vs Spectrum', comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Analisis Engineering

Pola getaran periodik → spike simetris pada spektrum.

Parameter resolusi citra memengaruhi resolusi frekuensi:

$$
\Delta f = \frac{1}{N}
$$

Semakin besar resolusi spasial, semakin presisi resolusi frekuensi.

---

# 8. Analisis Sistem dan Risiko Desain

### Sensitivitas Parameter

Cutoff kecil:
- Blur kuat
- Hilang detail
- Segmentasi gagal

Cutoff besar:
- Noise tidak tereduksi

### Dampak terhadap Pipeline

Filtering frekuensi memengaruhi:

- Canny edge detection
- Contour extraction
- Feature matching
- OCR recognition rate

### Dampak Topologi

High-pass ekstrem:
- Memutus konektivitas objek
- Mengubah Euler number

Low-pass ekstrem:
- Menggabungkan objek terpisah

---

# 9. Ringkasan Engineering

Transformasi Fourier menyediakan kerangka analisis global berbasis dekomposisi sinusoidal. Secara matematis, ia merepresentasikan citra sebagai superposisi frekuensi. Secara engineering, ia memungkinkan filtering global efisien, deteksi noise periodik, dan analisis tekstur.

Namun, parameter cutoff dan desain mask secara langsung memengaruhi struktur geometris citra. Kesalahan desain dapat merusak topologi objek dan mengganggu tahap lanjutan seperti contour analysis, OCR, maupun feature matching.

Domain frekuensi cocok untuk gangguan periodik dan filtering global. Tidak cocok untuk operasi lokal adaptif atau segmentasi berbasis konteks semantik.

---

# 10. Mini Project Lanjutan

1. Implementasi Butterworth filter dan analisis ringing effect  
2. Bandingkan Gaussian spatial vs FFT Gaussian untuk kernel besar  
3. Bangun sistem otomatis deteksi spike spektrum  
4. Analisis pengaruh cutoff terhadap akurasi OCR  
5. Integrasi FFT filtering dengan ORB feature matching  
6. Hitung perubahan Euler number sebelum dan sesudah filtering  
7. Buat GUI interaktif untuk kontrol cutoff frequency  
8. Bandingkan kompleksitas runtime berbagai resolusi  
9. Terapkan band-pass filter untuk analisis tekstur kain industri  
10. Implementasi adaptive notch filter berbasis peak detection  

---