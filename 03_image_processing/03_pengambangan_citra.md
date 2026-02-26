# 3.3 Pengambangan Citra (Thresholding)

Pengambangan (thresholding) adalah teknik segmentasi paling dasar dalam pemrosesan citra. Tujuannya adalah memisahkan objek dari latar belakang berdasarkan nilai intensitas piksel.

Walaupun terlihat sederhana, thresholding memiliki dasar statistik yang kuat dan menjadi fondasi bagi banyak sistem computer vision modern.

---

# 3.3.1 Dasar Teori

Sebuah citra grayscale dapat direpresentasikan sebagai fungsi:

```
f(x, y)
```

dengan nilai intensitas diskrit:

```
f(x, y) ∈ {0, 1, 2, ..., 255}
```

Distribusi nilai intensitas ini dapat dianalisis menggunakan **histogram**, yaitu estimasi distribusi probabilitas diskrit dari intensitas piksel.

Histogram citra:

```
h(i) = jumlah piksel dengan intensitas i
```

Jika dinormalisasi:

```
p(i) = h(i) / N
```

dengan N adalah total jumlah piksel.

Thresholding bertujuan membagi domain intensitas menjadi dua kelas:

- C0 → latar belakang
- C1 → objek

Dengan suatu nilai ambang T:

```
g(x, y) = 0  jika f(x, y) < T
g(x, y) = 255 jika f(x, y) ≥ T
```

Masalah utama: bagaimana menentukan T yang optimal?

---

# 3.3.2 Separability dan Variansi Antar Kelas

Dalam citra dengan dua objek berbeda, histogram sering menunjukkan dua puncak (bimodal). Nilai ambang optimal berada di antara kedua puncak tersebut.

Otsu mengusulkan pendekatan statistik:

Memaksimalkan variansi antar kelas (between-class variance).

Definisi:

- ω0 = probabilitas kelas 0
- ω1 = probabilitas kelas 1
- μ0 = rata-rata kelas 0
- μ1 = rata-rata kelas 1
- μT = rata-rata total

Variansi antar kelas:

```
σ_b² = ω0 ω1 (μ0 - μ1)²
```

Nilai T optimal adalah yang memaksimalkan σ_b².

Secara intuitif:
Semakin besar jarak rata-rata dua kelas, semakin baik pemisahannya.

---

# 3.3.3 Thresholding Global

## Struktur Fungsi

```
cv2.threshold(src, thresh, maxval, type)
```

Parameter:

- `thresh` → nilai ambang
- `maxval` → nilai pengganti (biasanya 255)
- `type` → tipe thresholding

Tipe:

- `THRESH_BINARY`
- `THRESH_BINARY_INV`
- `THRESH_TRUNC`
- `THRESH_TOZERO`
- `THRESH_TOZERO_INV`

---

## Contoh Dasar — Threshold Global

### Fokus Pembelajaran
- Memahami pemisahan biner
- Mengamati efek perubahan T

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)

_, t90  = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY)
_, t127 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
_, t160 = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)

comparison = np.hstack((img, t90, t127, t160))

cv2.imshow("Original | T=90 | T=127 | T=160", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```


### Insight Penting

- Nilai 127 dipilih manual.
- Jika histogram tidak bimodal, hasil bisa buruk.
- Sensitif terhadap pencahayaan.

### Kaitan Teknik

Digunakan dalam:
- Segmentasi dokumen hitam-putih
- Deteksi objek kontras tinggi
- Preprocessing OCR sederhana

---

# 3.3.4 Otsu Thresholding

Otsu secara otomatis mencari nilai T optimal berdasarkan histogram.

## Contoh — Otsu

### Fokus Pembelajaran
- Memahami optimasi variansi antar kelas
- Membandingkan threshold manual vs otomatis

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)

_, manual = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

ret, otsu = cv2.threshold(
    img, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

print("Threshold optimal:", ret)

comparison = np.hstack((img, manual, otsu))

cv2.imshow("Original | Manual 127 | Otsu", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight Penting

- Parameter thresh diabaikan (diisi 0).
- OpenCV menghitung histogram secara internal.
- Cocok untuk citra bimodal.
- Kurang efektif jika distribusi intensitas overlap berat.

### Kaitan Teknik

Digunakan dalam:
- Segmentasi medis sederhana
- Deteksi partikel industri
- Identifikasi objek latar belakang kontras

---

# 3.3.5 Adaptive Thresholding

Masalah global threshold:
Tidak stabil terhadap pencahayaan tidak merata.

Solusi: threshold lokal.

OpenCV menyediakan:

```
cv2.adaptiveThreshold()
```

## Contoh — Adaptive

### Fokus Pembelajaran
- Memahami threshold lokal berbasis neighborhood

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)

mean_adapt = cv2.adaptiveThreshold(
    img, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    11, 2
)

gauss_adapt = cv2.adaptiveThreshold(
    img, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11, 2
)

comparison = np.hstack((img, mean_adapt, gauss_adapt))

cv2.imshow("Original | Adaptive Mean | Adaptive Gaussian", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight Penting

- 11 → ukuran blok neighborhood
- 2 → konstanta pengurang
- Cocok untuk pencahayaan tidak merata

### Kaitan Teknik

Digunakan dalam:
- Scanner dokumen mobile
- Deteksi tulisan papan tulis
- Segmentasi objek di kondisi cahaya ekstrem

---

# 3.3.6 Adaptive Thresholding Lanjutan — Metode Sauvola

Adaptive thresholding pada OpenCV (`ADAPTIVE_THRESH_MEAN_C` dan `ADAPTIVE_THRESH_GAUSSIAN_C`) menggunakan rata-rata lokal sebagai dasar penentuan ambang.

Namun dalam banyak kasus dunia nyata — terutama pada dokumen lama atau citra dengan kontras rendah — metode ini belum cukup robust.

Salah satu metode yang lebih kuat adalah **Sauvola Thresholding**.

---

## Latar Belakang Teori

Metode Sauvola dikembangkan untuk segmentasi dokumen dengan variasi pencahayaan dan kontras lokal rendah.

Berbeda dengan adaptive mean biasa, Sauvola mempertimbangkan:

- Rata-rata lokal μ(x, y)
- Standar deviasi lokal σ(x, y)

Rumus ambang Sauvola:

```
T(x, y) = μ(x, y) * [ 1 + k * ( (σ(x, y) / R) - 1 ) ]
```

Keterangan:

- μ(x, y) → rata-rata intensitas pada window lokal
- σ(x, y) → standar deviasi pada window lokal
- R → nilai dinamis maksimum standar deviasi (biasanya 128 untuk citra 8-bit)
- k → parameter sensitivitas (biasanya 0.2 – 0.5)

---

## Intuisi Engineering

Mengapa memasukkan standar deviasi?

Karena standar deviasi mencerminkan tingkat kontras lokal.

Jika kontras tinggi:
→ σ besar  
→ threshold lebih tinggi  

Jika kontras rendah:
→ σ kecil  
→ threshold lebih rendah  

Artinya, Sauvola menyesuaikan ambang berdasarkan dinamika lokal, bukan hanya rata-rata.

Ini membuatnya jauh lebih stabil terhadap:

- Shadow
- Background kertas tua
- Noda pada dokumen
- Pencahayaan tidak merata

---

## Perbandingan Mean vs Sauvola

Adaptive Mean:

```
T(x,y) = μ(x,y) - C
```

Sauvola:

```
T(x,y) bergantung pada μ dan σ
```

Sauvola lebih adaptif terhadap variasi tekstur.

---

## Implementasi Sauvola di Python

OpenCV belum menyediakan Sauvola secara langsung, tetapi dapat diimplementasikan menggunakan NumPy atau menggunakan library `scikit-image`.

Contoh implementasi sederhana menggunakan scikit-image:

```python
import cv2
from skimage.filters import threshold_sauvola
import numpy as np

img = cv2.imread("anu.jpeg", 0)

window_size = 25
k = 0.3

sauvola_thresh = threshold_sauvola(img, window_size=window_size, k=k)
sauvola = (img > sauvola_thresh).astype(np.uint8) * 255

comparison = np.hstack((img, sauvola))

cv2.imshow("Original | Sauvola", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Fokus Pembelajaran

- Memahami peran standar deviasi lokal
- Memahami pengaruh parameter k
- Mengamati perbedaan hasil terhadap adaptive mean

---

## Insight Penting

- Window size besar → lebih stabil, kurang sensitif detail kecil
- Window size kecil → lebih sensitif noise
- Parameter k mengontrol agresivitas segmentasi
- Sauvola lebih mahal secara komputasi dibanding mean

---

## Kapan Menggunakan Sauvola?

Sangat cocok untuk:

- OCR dokumen lama
- Arsip sejarah
- Citra tulisan tangan
- Segmentasi teks papan tulis
- Dokumen dengan background tekstur

Kurang cocok untuk:

- Objek kontras tinggi sederhana
- Sistem real-time dengan keterbatasan komputasi

---

## Analisis Kompleksitas

Adaptive mean:
O(N)

Sauvola:
O(N * window_size²)

Namun dapat dioptimasi dengan integral image untuk komputasi cepat rata-rata dan variansi lokal.

---

## Insight Akademik

Metode Sauvola adalah bentuk thresholding berbasis statistik lokal yang mempertimbangkan distribusi intensitas dalam neighborhood.

Secara konseptual, ini mendekati pendekatan klasifikasi berbasis fitur lokal sederhana.

Ini menunjukkan evolusi thresholding dari:

Global → Local Mean → Variance-Aware Thresholding.

Metode ini menjadi jembatan menuju pendekatan segmentasi berbasis machine learning.

---

# 3.3.7 Studi Kasus Teknik — Thresholding pada Berbagai Skenario Nyata

Thresholding jarang digunakan dalam kondisi ideal. Di dunia nyata, kita menghadapi variasi pencahayaan, noise, tekstur latar, dan kontras rendah. Berikut beberapa studi kasus teknik dengan pendekatan yang berbeda.

---

# Kasus 1 — Inspeksi Komponen Industri (Noise + Refleksi)

## Permasalahan

- Permukaan logam reflektif
- Pencahayaan tidak merata
- Noise sensor
- Background tidak sepenuhnya gelap

Threshold global sering gagal karena histogram overlap.

## Pipeline Engineering

1. Grayscale
2. Gaussian blur
3. Otsu
4. Morphological opening

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5,5), 0)

_, otsu = cv2.threshold(
    blur, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

kernel = np.ones((3,3), np.uint8)
clean = cv2.morphologyEx(otsu, cv2.MORPH_OPEN, kernel)

comparison = np.hstack((gray, otsu, clean))

cv2.imshow("Gray | Otsu | After Morphology", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight

Preprocessing menentukan kualitas segmentasi.  
Otsu bekerja lebih stabil setelah noise dikurangi.

---

# Kasus 2 — Scanner Dokumen dengan Shadow

## Permasalahan

- Bayangan tangan
- Pencahayaan tidak merata
- Background kertas tidak homogen

Threshold global → gagal total.

## Solusi: Adaptive + Sauvola

```python
import cv2
from skimage.filters import threshold_sauvola
import numpy as np

img = cv2.imread("anu.jpeg", 0)

mean_adapt = cv2.adaptiveThreshold(
    img, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    21, 5
)

window_size = 25
k = 0.3
sauvola_thresh = threshold_sauvola(img, window_size=window_size, k=k)
sauvola = (img > sauvola_thresh).astype(np.uint8) * 255

comparison = np.hstack((img, mean_adapt, sauvola))

cv2.imshow("Original | Adaptive Mean | Sauvola", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```


### Insight

- Sauvola mempertimbangkan kontras lokal.
- Sangat efektif untuk teks dengan background tidak merata.
- Cocok untuk OCR pipeline.

---

# Kasus 3 — Deteksi Api Berbasis Intensitas Tinggi

## Permasalahan

Pada sistem monitoring kebakaran, api memiliki intensitas tinggi pada channel tertentu.

Pendekatan sederhana:
Threshold pada channel merah atau brightness tinggi.

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

red_channel = img[:,:,2]

_, fire_mask = cv2.threshold(red_channel, 200, 255, cv2.THRESH_BINARY)

comparison = np.hstack((red_channel, fire_mask))

cv2.imshow("Red Channel | Fire Mask", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight

- Thresholding bisa digunakan untuk deteksi cepat.
- Tidak cukup robust tanpa filtering warna tambahan.
- Biasanya dikombinasikan dengan HSV threshold.

---

# Kasus 4 — Segmentasi Sel Mikroskop

## Permasalahan

- Background terang
- Sel memiliki kontras tipis
- Noise tinggi

## Strategi

1. Gaussian blur
2. Adaptive threshold
3. Closing untuk mengisi lubang kecil

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)

blur = cv2.GaussianBlur(img, (7,7), 0)

adaptive = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    11,
    2
)

kernel = np.ones((3,3), np.uint8)
closing = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel)

comparison = np.hstack((img, adaptive, closing))

cv2.imshow("Original | Adaptive | After Closing", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight

- THRESH_BINARY_INV sering diperlukan jika objek lebih gelap dari background.
- Morfologi penting untuk menyatukan region objek.

---

# Analisis Perbandingan Engineering

| Kasus | Metode | Tantangan Utama |
|-------|--------|----------------|
| Industri | Otsu + Morphology | Noise & refleksi |
| Dokumen | Sauvola | Shadow & kontras lokal |
| Api | Channel Threshold | False positive |
| Mikroskop | Adaptive + Morphology | Kontras rendah |

---

# Pelajaran Engineering dari Studi Kasus

1. Thresholding jarang berdiri sendiri.
2. Preprocessing menentukan keberhasilan.
3. Distribusi histogram sangat penting.
4. Local statistics lebih kuat dari global.
5. Morfologi hampir selalu diperlukan.
6. Segmentasi adalah pipeline, bukan satu fungsi.
7. Evaluasi kuantitatif penting dalam sistem nyata.
8. Setiap domain memiliki karakteristik berbeda.

---

Thresholding adalah teknik sederhana, tetapi dalam sistem teknik yang serius, ia selalu menjadi bagian dari pipeline yang lebih besar.

---

# 3.3.8 Analisis Kegagalan Thresholding

Thresholding akan gagal jika:

1. Histogram tidak bimodal
2. Objek dan background memiliki distribusi overlap
3. Pencahayaan ekstrem
4. Refleksi permukaan
5. Shadow kuat

Contoh kegagalan:

- Citra wajah dengan pencahayaan samping
- Objek berwarna tetapi intensitas sama
- Citra medis dengan kontras rendah

Dalam kasus seperti ini, solusi lebih lanjut diperlukan:

- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Edge-based segmentation
- Clustering (K-means)
- Deep learning segmentation

---

# 3.3.9 Evaluasi Kualitas Segmentasi

Dalam sistem teknik, kita tidak cukup berkata "hasilnya terlihat bagus".

Beberapa metrik evaluasi:

- IoU (Intersection over Union)
- Dice coefficient
- Precision-Recall
- Confusion matrix (pixel-wise)

Thresholding adalah classifier biner 1D. Maka evaluasinya dapat dilakukan seperti klasifikasi biasa.

---

# Ringkasan Engineering Tambahan

1. Thresholding adalah klasifikasi berbasis intensitas.
2. Histogram adalah estimasi distribusi probabilitas.
3. Otsu memaksimalkan variansi antar kelas.
4. Adaptive threshold bekerja lokal.
5. Noise merusak separability.
6. Preprocessing meningkatkan performa.
7. Pipeline lebih penting daripada satu teknik.
8. Morfologi membersihkan hasil segmentasi.
9. Evaluasi kuantitatif diperlukan.
10. Thresholding adalah fondasi segmentasi lanjutan.

---

# Ide Mini Project Tingkat Lanjut

1. Sistem inspeksi cacat logam.
2. Penghitungan objek otomatis pada conveyor.
3. Scanner dokumen real-time dengan adaptive threshold.
4. Segmentasi sel mikroskop dan penghitungan jumlah sel.
5. Analisis distribusi histogram dataset Anda.
6. Eksperimen pengaruh noise terhadap Otsu.
7. Perbandingan global vs adaptive pada dataset nyata.
8. Sistem deteksi api berbasis threshold warna.
9. Evaluasi IoU hasil segmentasi.
10. Dashboard analisis separability histogram.