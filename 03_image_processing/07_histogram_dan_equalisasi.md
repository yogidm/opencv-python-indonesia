# 3.7 Histogram dan Equalisasi Citra

---

## 1. Pendahuluan Teoretis

Setelah pembahasan deteksi tepi yang berfokus pada turunan spasial dan perubahan gradien intensitas, tahap selanjutnya dalam pengolahan citra adalah analisis distribusi statistik intensitas melalui histogram. Jika deteksi tepi bekerja pada domain diferensial spasial, maka histogram bekerja pada domain probabilistik intensitas global.

Misalkan citra grayscale didefinisikan sebagai fungsi diskrit:

$$
I : \Omega \subset \mathbb{Z}^2 \rightarrow \{0,1,\dots,L-1\}
$$

dengan:

- $\Omega$ adalah domain piksel berukuran $M \times N$
- $L$ adalah jumlah level intensitas (untuk citra 8-bit, $L=256$)
- $I(x,y)$ adalah nilai intensitas pada koordinat $(x,y)$

Histogram didefinisikan sebagai fungsi frekuensi:

$$
h(k) = |\{(x,y) \in \Omega \mid I(x,y) = k\}|
$$

yang menyatakan jumlah piksel dengan intensitas $k$.

Jika dinormalisasi:

$$
p(k) = \frac{h(k)}{MN}
$$

maka $p(k)$ adalah estimasi fungsi massa probabilitas (Probability Mass Function / PMF) dari distribusi intensitas citra.

### Interpretasi Matematis

Histogram adalah estimasi empiris distribusi probabilitas diskrit dari intensitas. Jika distribusi sempit dan terpusat, maka variansi rendah dan kontras citra rendah.

Variansi intensitas didefinisikan sebagai:

$$
\sigma^2 = \sum_{k=0}^{L-1} (k - \mu)^2 p(k)
$$

dengan:

$$
\mu = \sum_{k=0}^{L-1} k \cdot p(k)
$$

adalah rata-rata intensitas.

### Interpretasi Engineering

- Histogram lebar → kontras tinggi
- Histogram sempit → kontras rendah
- Histogram bimodal → cocok untuk thresholding
- Histogram skewed → iluminasi tidak merata

Histogram menjadi dasar bagi normalisasi kontras sebelum tahap lanjutan seperti thresholding, contour detection, atau OCR.

---

## 2. Equalisasi Histogram Global

Tujuan equalisasi histogram adalah melakukan transformasi intensitas non-linear sehingga distribusi output mendekati distribusi uniform.

Didefinisikan fungsi distribusi kumulatif (CDF):

$$
c(k) = \sum_{i=0}^{k} p(i)
$$

Transformasi intensitas:

$$
s = T(k) = (L-1) \cdot c(k)
$$

dengan:

- $T(k)$ adalah fungsi transformasi
- $s$ adalah intensitas baru
- $(L-1)$ adalah skala maksimum intensitas

Transformasi ini bersifat monotonik non-decreasing, sehingga menjaga urutan intensitas.

### Makna Matematis

CDF memetakan domain intensitas ke interval $[0,1]$. Dengan mengalikan $(L-1)$, distribusi diratakan secara global.

### Makna Engineering

- Meningkatkan dynamic range
- Memperbaiki kontras global
- Tidak mempertimbangkan konteks lokal
- Rentan terhadap amplifikasi noise

Kompleksitas komputasi:  
Perhitungan histogram $O(MN)$  
Transformasi piksel $O(MN)$  
Total linear terhadap jumlah piksel.

---

## 3. Implementasi OpenCV — Equalisasi Global

Struktur fungsi:

```python
cv2.equalizeHist(src)
```

Parameter:
- `src`: citra grayscale 8-bit

Fungsi ini tidak mendukung citra warna secara langsung.

### Contoh Implementasi

```python
import cv2
import numpy as np

img = cv2.imread('input.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

equalized = cv2.equalizeHist(gray)

comparison = np.hstack((gray, equalized))

cv2.imshow('Original vs Equalized', comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 4. Adaptive Histogram Equalization (CLAHE)

Global equalization gagal ketika iluminasi tidak merata. Solusinya adalah CLAHE (Contrast Limited Adaptive Histogram Equalization).

Citra dibagi menjadi blok berukuran $m \times n$.  
Histogram dihitung secara lokal.

Untuk mencegah noise amplification:

$$
h_{clipped}(k) = \min(h(k), T_{clip})
$$

Excess histogram didistribusikan ulang secara merata.

Parameter penting:

- `clipLimit`
- `tileGridSize`

### Struktur Fungsi

```python
cv2.createCLAHE(clipLimit, tileGridSize)
```

### Implementasi

```python
import cv2
import numpy as np

img = cv2.imread('input.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
adaptive = clahe.apply(gray)

comparison = np.hstack((gray, adaptive))

cv2.imshow('Original vs CLAHE', comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 5. Studi Kasus 1 — Citra Medis X-Ray

### Permasalahan Lapangan

Citra radiografi memiliki kontras rendah dan distribusi intensitas terpusat sempit.

### Pipeline

Grayscale → CLAHE → Canny Edge → Analisis Kontur

```python
import cv2
import numpy as np

img = cv2.imread('xray.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)

edges = cv2.Canny(enhanced, 50, 150)

comparison = np.hstack((gray, enhanced, edges))

cv2.imshow('Xray Pipeline', comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Analisis Engineering

- CLAHE meningkatkan visibilitas struktur tulang
- clipLimit tinggi meningkatkan noise granular
- Edge detection menjadi lebih stabil

---

## 6. Studi Kasus 2 — Preprocessing OCR Dokumen

### Permasalahan

Dokumen buram dengan iluminasi tidak merata menyebabkan threshold gagal.

### Pipeline

Grayscale → CLAHE → Otsu Threshold

```python
import cv2
import numpy as np

img = cv2.imread('document.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
enhanced = clahe.apply(gray)

_, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

comparison = np.hstack((gray, enhanced, thresh))

cv2.imshow('OCR Preprocessing', comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Analisis

Distribusi yang lebih merata meningkatkan stabilitas threshold global.

---

## 7. Studi Kasus 3 — Sistem Kamera Kendaraan Malam Hari

### Permasalahan

Low illumination menyebabkan fitur tidak terdeteksi.

### Pipeline

Frame → CLAHE → ORB Feature Detection

```python
import cv2
import numpy as np

img = cv2.imread('night.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)

orb = cv2.ORB_create()
kp, des = orb.detectAndCompute(enhanced, None)

output = cv2.drawKeypoints(enhanced, kp, None)

comparison = np.hstack((gray, enhanced, output))

cv2.imshow('Night Vision Enhancement', comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Analisis Engineering

- Jumlah keypoint meningkat
- Terlalu agresif meningkatkan false feature
- Trade-off antara kontras dan stabilitas descriptor

---

## 8. Analisis Sistem dan Dampak Lanjutan

### Sensitivitas Parameter

clipLimit kecil → kontras rendah  
clipLimit besar → noise meningkat  

tileGrid kecil → adaptif tinggi, mahal komputasi  
tileGrid besar → mendekati global equalization  

### Dampak terhadap Topologi

Equalization tidak mengubah struktur spasial, namun mempengaruhi:

- Jumlah connected component setelah threshold
- Stabilitas contour
- Distribusi gradien untuk edge detector

### Dampak ke Tahap Pipeline

- Meningkatkan performa thresholding
- Meningkatkan jumlah feature point
- Meningkatkan robustness deteksi objek dalam kondisi low light
- Dapat mengganggu segmentasi jika noise dominan

---

## 9. Ringkasan Engineering

Histogram adalah representasi statistik global dari distribusi intensitas.  
Equalisasi adalah transformasi non-linear berbasis CDF untuk memperluas dynamic range.

Dalam sistem nyata:

- Gunakan global equalization untuk iluminasi homogen
- Gunakan CLAHE untuk iluminasi tidak merata
- Selalu evaluasi dampak terhadap noise
- Validasi terhadap tahap lanjutan (contour, OCR, feature detection)

Kesalahan parameter dapat menyebabkan:
- Noise amplification
- False edge
- Instabilitas segmentasi
- Penurunan performa model AI

---

## 10. Mini Project Eksperimental

1. Analisis perubahan variansi sebelum dan sesudah equalization  
2. Evaluasi jumlah keypoint ORB terhadap variasi clipLimit  
3. Bandingkan performa OCR dengan dan tanpa CLAHE  
4. Uji histogram equalization pada video real-time  
5. Analisis distribusi gradien sebelum dan sesudah transformasi  
6. Integrasikan CLAHE dengan Gaussian Blur  
7. Evaluasi pengaruh tileGridSize terhadap waktu komputasi  
8. Analisis perubahan jumlah connected component  
9. Kombinasikan CLAHE dengan adaptive threshold  
10. Benchmark CPU vs GPU untuk equalization  

---

Bab ini menghubungkan analisis statistik intensitas dengan peningkatan kualitas sinyal visual sebelum tahap ekstraksi fitur lanjutan dalam pipeline computer vision