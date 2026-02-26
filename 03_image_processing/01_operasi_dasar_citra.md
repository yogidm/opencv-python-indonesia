# 3.1 Operasi Dasar Citra Digital

Operasi dasar citra adalah manipulasi langsung terhadap nilai piksel. Pada tahap ini, kita belum masuk ke transformasi spasial atau filtering berbasis kernel, tetapi memahami bagaimana citra direpresentasikan dan dimodifikasi pada level matriks. Semua teknik lanjutan dalam computer vision — mulai dari thresholding, filtering, hingga deep learning — pada akhirnya tetap bergantung pada manipulasi nilai piksel. Oleh karena itu, pemahaman operasi dasar ini menjadi fondasi matematis dan komputasional dari seluruh pipeline pengolahan citra.

Sebuah citra grayscale direpresentasikan sebagai matriks dua dimensi:

```
f(x, y)
```

Sedangkan citra warna direpresentasikan sebagai matriks tiga dimensi:

```
f(x, y, c)
```

dengan `c` adalah kanal warna (B, G, R pada OpenCV).

Pemahaman struktur ini sangat penting sebelum masuk ke tahap pengolahan yang lebih kompleks.

---

# 3.1.1 Akses dan Modifikasi Piksel

## Fokus Pembelajaran
- Memahami representasi matriks citra
- Mengakses nilai piksel tertentu
- Mengamati efek perubahan langsung

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

# Salinan untuk modifikasi
modified = img.copy()

# Ubah piksel di lokasi tertentu menjadi putih
modified[100, 100] = [255, 255, 255]

comparison = np.hstack((img, modified))

cv2.imshow("Left: Original | Right: Modified Pixel", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Insight Penting

- Indeks piksel adalah `[y, x]`, bukan `[x, y]`.
- Untuk citra warna: formatnya BGR.
- Perubahan satu piksel hampir tidak terlihat secara global.
- Operasi per-piksel dengan loop Python tidak efisien untuk citra besar.

## Kaitan Teknik

Digunakan untuk:
- Debugging sistem
- Visualisasi titik fitur
- Menandai koordinat penting dalam sistem tracking

---

# 3.1.2 Region of Interest (ROI)

Dalam sistem pemrosesan citra nyata, tidak semua bagian citra memiliki nilai informasi yang sama. Sering kali, hanya area tertentu yang relevan terhadap tujuan sistem. Konsep inilah yang dikenal sebagai **Region of Interest (ROI)**.

ROI adalah subset dari domain spasial citra yang dipilih untuk diproses lebih lanjut. Secara matematis, jika citra direpresentasikan sebagai fungsi:

```
f(x, y)
```

maka ROI adalah pembatasan domain:

```
f(x, y),  untuk (x, y) ∈ Ω
```

di mana Ω adalah himpunan koordinat piksel yang dipilih.

Dengan kata lain, kita tidak lagi bekerja pada seluruh matriks citra, tetapi hanya pada sub-matriks tertentu.

---

## Mengapa ROI Penting dalam Sistem Teknik?

Dalam sistem vision real-time, pemrosesan seluruh frame beresolusi tinggi dapat menjadi mahal secara komputasi. Sebagai contoh:

- Kamera 1920×1080 → ~2 juta piksel
- Proses konvolusi 5×5 → 25 operasi per piksel
- Total operasi per frame → puluhan juta

Jika hanya 20% area yang relevan, penggunaan ROI dapat mengurangi beban komputasi secara signifikan.

ROI juga penting dalam:

- Face detection (hanya proses area wajah)
- Tracking objek bergerak
- Sistem inspeksi industri (fokus pada area conveyor)
- Vehicle detection (hanya area jalan)

---

## Fokus Pembelajaran

- Memahami slicing matriks sebagai pembatasan domain
- Memahami bahwa ROI adalah referensi (bukan selalu salinan)
- Mengamati dampak manipulasi lokal terhadap citra global

---

## Contoh — Manipulasi ROI

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

roi_img = img.copy()

# Ambil sebagian citra
roi = roi_img[100:200, 150:300]

# Tempelkan ROI ke lokasi lain
roi_img[0:100, 0:150] = roi

comparison = np.hstack((img, roi_img))

cv2.imshow("Left: Original | Right: ROI Manipulated", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Insight Penting

- Format slicing adalah `[row_start:row_end, col_start:col_end]`
- ROI pada NumPy adalah view (referensi memori), bukan salinan baru.
- Gunakan `.copy()` jika ingin salinan independen.
- ROI memungkinkan manipulasi lokal tanpa memproses seluruh citra.
- Konsep ini menjadi dasar sliding window pada deteksi objek klasik.

---

## Kaitan Teknik

ROI digunakan dalam:

1. Tracking berbasis bounding box
2. Sistem vision robotik untuk fokus area kerja
3. Analisis citra medis (area tumor)
4. Deteksi plat nomor (fokus area bawah kendaraan)
5. Augmented reality untuk overlay lokal


ROI bukan sekadar teknik slicing, tetapi strategi optimasi sistem vision.

---

# 3.1.3 Operasi Aritmetika — Penambahan Intensitas

Penambahan intensitas merupakan transformasi linier sederhana yang meningkatkan brightness citra. Secara matematis:

$$
g(x,y) = f(x,y) + k
$$

dengan:

- $f(x,y)$ adalah citra asli  
- $k$ adalah konstanta positif  
- $g(x,y)$ adalah citra hasil  

Transformasi ini menaikkan seluruh nilai piksel sebesar $k$ selama tidak terjadi saturasi.

---

## Analisis Distribusi Intensitas

Ketika intensitas ditambahkan:

- Histogram citra bergeser ke kanan.
- Nilai rata-rata (mean) meningkat.
- Variansi relatif tetap jika tidak terjadi clipping.

Namun karena citra 8-bit memiliki batas maksimum 255, maka jika:

$$
f(x,y) + k > 255
$$

nilai akan dipotong menjadi 255 (saturasi).

Clipping menyebabkan penyempitan **dynamic range efektif** dan kehilangan detail pada area terang.

Dynamic range didefinisikan sebagai:

$$
DR = I_{max} - I_{min}
$$

Jika banyak piksel mencapai 255, maka informasi highlight akan hilang.

---

## Dampak terhadap Thresholding

Misalkan digunakan threshold $T = 120$.

Jika suatu piksel memiliki nilai 90, setelah ditambah 50:

$$
90 + 50 = 140
$$

Piksel tersebut kini melewati threshold.

Artinya, operasi brightness dapat mengubah hasil segmentasi. Oleh karena itu, penyesuaian intensitas harus dipertimbangkan dalam pipeline preprocessing.

---

## Fokus Pembelajaran

- Memahami penambahan intensitas sebagai transformasi linier.
- Mengamati pergeseran histogram.
- Memahami fenomena saturasi (clipping).
- Menganalisis dampaknya terhadap segmentasi.

---

## Contoh Implementasi

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

bright = cv2.add(img, 50)

comparison = np.hstack((img, bright))

cv2.imshow("Left: Original | Right: Brighter", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Insight Penting

- Gunakan `cv2.add()` untuk mencegah overflow.
- Saturasi menjaga nilai maksimum tetap 255.
- Histogram bergeser ke kanan.
- Brightness memengaruhi thresholding dan segmentasi.

---

## Kaitan Teknik

Digunakan dalam:

- Preprocessing sebelum threshold  
- Koreksi pencahayaan rendah  
- Normalisasi dataset  
- Penyesuaian eksposur sistem kamera  


---

# 3.1.4 Operasi Pengurangan Intensitas

Pengurangan intensitas adalah transformasi linier yang menurunkan brightness citra:

$$
g(x,y) = f(x,y) - k
$$

dengan $k$ konstanta positif.

---

## Analisis Distribusi Intensitas

Ketika intensitas dikurangi:

- Histogram bergeser ke kiri.
- Nilai rata-rata menurun.
- Jika $f(x,y) - k < 0$, maka terjadi clipping ke 0.

Clipping pada area gelap menyebabkan kehilangan detail pada region bayangan.

Dynamic range menyempit jika banyak piksel mencapai 0.

---

## Dampak terhadap Segmentasi

Jika threshold digunakan pada nilai $T = 120$:

- Piksel yang sebelumnya sedikit di atas threshold dapat turun di bawah threshold.
- Hasil segmentasi dapat berubah signifikan.

Operasi ini sering digunakan untuk simulasi kondisi low-light dan pengujian robustness sistem vision terhadap variasi pencahayaan.

---

## Fokus Pembelajaran

- Memahami transformasi linier negatif.
- Mengamati histogram bergeser ke kiri.
- Memahami clipping ke nol.
- Menghubungkan perubahan brightness dengan segmentasi.

---

## Contoh Implementasi

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

dark = cv2.subtract(img, 50)

comparison = np.hstack((img, dark))

cv2.imshow("Left: Original | Right: Darker", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Insight Penting

- Gunakan `cv2.subtract()` untuk mencegah underflow.
- Nilai minimum dijaga pada 0.
- Histogram bergeser ke kiri.
- Perubahan brightness dapat memengaruhi threshold.

---

## Kaitan Teknik

Digunakan dalam:

- Simulasi kondisi gelap  
- Analisis robustness algoritma  
- Pengujian segmentasi  
- Pipeline low-light enhancement  

---
# 3.1.5 Operasi Logika

Operasi logika pada citra bekerja pada level bit dari setiap piksel. Dalam konteks pemrosesan citra, operasi ini sering digunakan untuk melakukan **masking**, yaitu mempertahankan bagian tertentu dari citra dan menghilangkan bagian lainnya.

Jika citra dianggap sebagai matriks nilai diskrit, maka operasi bitwise dapat dipandang sebagai operasi Boolean antar piksel yang bersesuaian.

Untuk dua citra A dan B dengan ukuran sama:

```
C(x, y) = A(x, y) AND B(x, y)
```

Pada citra biner (0 dan 255), operasi ini setara dengan operasi himpunan:

- AND → irisan (intersection)
- OR → gabungan (union)
- NOT → komplemen
- XOR → beda simetris

Dengan demikian, operasi bitwise bukan hanya manipulasi piksel, tetapi juga dapat ditafsirkan sebagai operasi teori himpunan pada domain citra.

---

## Konsep Masking

Mask adalah citra biner yang menentukan area mana yang dipertahankan.

Aturan sederhana:

- Piksel mask = 255 → piksel asli dipertahankan
- Piksel mask = 0 → piksel dihapus (menjadi hitam)

Secara matematis:

```
g(x, y) = f(x, y) jika mask(x, y) = 255
g(x, y) = 0       jika mask(x, y) = 0
```

Masking adalah operasi seleksi spasial.

## Fokus Pembelajaran

- Memahami operasi Boolean pada domain piksel
- Mengamati perbedaan AND, OR, XOR, NOT secara visual
- Menghubungkan operasi bitwise dengan teori himpunan

---

# Contoh 1 — Bitwise AND (Masking)

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

mask = np.zeros(img.shape[:2], dtype=np.uint8)
mask[100:300, 100:300] = 255

result = cv2.bitwise_and(img, img, mask=mask)

comparison = np.hstack((img, result))
cv2.imshow("Left: Original | Right: AND Mask", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight

AND mempertahankan hanya area putih pada mask.  
Secara himpunan: A ∩ B.

---

# Contoh 2 — Bitwise OR (Penggabungan Region)

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

mask1 = np.zeros(img.shape[:2], dtype=np.uint8)
mask1[50:200, 50:200] = 255

mask2 = np.zeros(img.shape[:2], dtype=np.uint8)
mask2[150:350, 150:350] = 255

or_mask = cv2.bitwise_or(mask1, mask2)

comparison = np.hstack((mask1, mask2, or_mask))

cv2.imshow("Mask1 | Mask2 | OR Result", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight

OR menggabungkan dua region.  
Secara himpunan: A ∪ B.  
Digunakan untuk menggabungkan hasil segmentasi berbeda.

---

# Contoh 3 — Bitwise XOR (Deteksi Perbedaan)

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

mask1 = np.zeros(img.shape[:2], dtype=np.uint8)
mask1[100:250, 100:250] = 255

mask2 = np.zeros(img.shape[:2], dtype=np.uint8)
mask2[150:300, 150:300] = 255

xor_mask = cv2.bitwise_xor(mask1, mask2)

comparison = np.hstack((mask1, mask2, xor_mask))

cv2.imshow("Mask1 | Mask2 | XOR Result", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight

XOR menampilkan area yang berbeda antara dua mask.  
Secara himpunan: A Δ B.  
Digunakan dalam change detection dan evaluasi segmentasi.

---

# Contoh 4 — Bitwise NOT (Komplemen)

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)

not_img = cv2.bitwise_not(img)

comparison = np.hstack((img, not_img))

cv2.imshow("Left: Original | Right: NOT", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight

NOT membalik nilai intensitas:  
0 → 255  
255 → 0  

Digunakan dalam:
- Inversi mask
- Penyesuaian pipeline morfologi
- Persiapan sebelum threshold inverse

---

# Analisis Engineering

| Operasi | Interpretasi Himpunan | Penggunaan Teknik |
|----------|----------------------|------------------|
| AND | Irisan | Masking, seleksi area |
| OR | Gabungan | Merge hasil segmentasi |
| XOR | Beda simetris | Deteksi perubahan |
| NOT | Komplemen | Inversi mask |

---

## Kaitan Teknik Lanjutan

Operasi bitwise menjadi fondasi bagi:

- Segmentasi multi-mask
- Sistem augmented reality
- Evaluasi IoU (intersection over union)
- Pipeline morfologi (erosi & dilasi)
- Tracking berbasis region

---

Operasi bitwise adalah jembatan antara representasi numerik citra dan teori himpunan dalam analisis bentuk.

---

# Ringkasan Bab 3.1 — Operasi Dasar Citra

1. Citra digital direpresentasikan sebagai matriks diskrit dua atau tiga dimensi yang berisi nilai intensitas.
2. Akses piksel menggunakan indeks `[y, x]`, di mana `y` adalah baris dan `x` adalah kolom.
3. Semua operasi citra pada dasarnya adalah manipulasi matriks numerik.
4. ROI merupakan pembatasan domain spasial untuk efisiensi komputasi dan fokus analisis.
5. ROI bekerja sebagai view (referensi memori), bukan selalu salinan independen.
6. Operasi aritmetika (add, subtract, multiply) memodifikasi distribusi intensitas.
7. Saturasi pada OpenCV (`cv2.add`) mencegah overflow numerik.
8. NumPy dapat menghasilkan wrap-around jika tidak dikontrol.
9. Operasi bitwise merepresentasikan operasi himpunan pada domain piksel.
10. Masking adalah bentuk seleksi spasial berbasis logika Boolean.
11. Histogram menggambarkan distribusi intensitas dan berubah setelah manipulasi citra.
12. Analisis before–after wajib dilakukan untuk evaluasi visual.
13. Kompleksitas komputasi meningkat proporsional dengan jumlah piksel.
14. ROI dan masking adalah strategi optimasi sistem vision real-time.
15. Operasi dasar menjadi fondasi transformasi geometris, filtering, morfologi, dan segmentasi.

Bab ini menegaskan bahwa computer vision pada level awal adalah persoalan manipulasi matriks yang terkontrol dan terukur.

---

# Ide Mini Project Berbasis Engineering

1. Sistem penyesuaian brightness interaktif berbasis trackbar.
2. ROI dinamis untuk optimasi pemrosesan frame video.
3. Analisis histogram sebelum–sesudah manipulasi intensitas.
4. Simulasi kondisi overexposure dan underexposure.
5. Perbandingan performa NumPy vs cv2.add pada overflow.
6. Sistem masking berbasis deteksi threshold.
7. Deteksi area terang otomatis dan pelabelan region.
8. Dashboard visual perbandingan manipulasi citra.
9. Eksperimen distribusi intensitas terhadap kontras.
10. Implementasi IoU sederhana berbasis bitwise AND dan OR.
11. Visualisasi perubahan histogram secara real-time.
12. Sistem seleksi area kerja robot berbasis ROI.
13. Change detection sederhana menggunakan XOR.
14. Segmentasi manual berbasis kombinasi threshold + masking.
15. Eksperimen efisiensi komputasi dengan dan tanpa ROI.

