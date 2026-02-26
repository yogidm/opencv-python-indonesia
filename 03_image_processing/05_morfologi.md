# 3.5 Operasi Morfologi (Morphological Operations)

Operasi morfologi adalah teknik pemrosesan citra berbasis **struktur geometris**.  
Berbeda dengan smoothing yang bekerja pada intensitas dan konvolusi linear, morfologi berasal dari teori himpunan dan aljabar matematika.

Morfologi terutama digunakan pada citra biner, tetapi dapat diperluas ke citra grayscale.

---

# 3.5.1 Fondasi Teori Morfologi

## Representasi Himpunan

Citra biner dapat direpresentasikan sebagai himpunan koordinat:

$$
A = \{(x,y) \mid f(x,y) = 1\}
$$

Artinya, setiap piksel putih dianggap sebagai anggota himpunan.

Kernel morfologi disebut **structuring element (SE)** dan direpresentasikan sebagai:

$$
B \subseteq \mathbb{Z}^2
$$

Structuring element adalah operator yang "menjelajahi" citra.

---

## Interpretasi Geometris

Jika thresholding adalah klasifikasi piksel, maka morfologi adalah manipulasi bentuk objek.

Operasi morfologi bekerja berdasarkan:

- Relasi inklusi himpunan
- Translasi kernel
- Operasi irisan dan gabungan

---

# 3.5.2 Erosi (Erosion)

## Definisi Matematis

Secara formal, erosi didefinisikan sebagai:

$$
A \ominus B = \{ z \in \mathbb{Z}^2 \mid B_z \subseteq A \}
$$

dengan:

- $A$ → himpunan piksel objek
- $B$ → structuring element
- $B_z$ → translasi kernel ke posisi $z$

Artinya, suatu piksel pada posisi $z$ akan tetap menjadi bagian objek **hanya jika seluruh kernel yang ditempatkan di posisi tersebut sepenuhnya berada di dalam objek**.

---

## Interpretasi Geometris

Bayangkan kernel sebagai “template penguji bentuk”.

Ketika kernel digeser ke seluruh citra:

- Jika kernel menyentuh area background → piksel pusat dihapus.
- Jika kernel sepenuhnya berada dalam objek → piksel dipertahankan.

Secara geometris, erosi:

- Mengurangi ketebalan objek
- Menghilangkan tonjolan kecil
- Menghapus noise berukuran lebih kecil dari kernel

Secara topologis, erosi dapat:

- Memutus objek tipis
- Mengubah konektivitas

---

## Interpretasi Komputasional

Untuk kernel berukuran $k \times k$:

- Kompleksitas ~ $O(N \cdot k^2)$
- Iterasi berulang setara dengan memperbesar ukuran kernel efektif

---

## Implementasi OpenCV

```
cv2.erode(src, kernel, iterations)
```

Parameter:
- `src` → citra input (biner/grayscale)
- `kernel` → structuring element
- `iterations` → jumlah pengulangan erosi

---

## Contoh — Erosi

```python
import cv2
import numpy as np

# Baca citra grayscale
img = cv2.imread("anu.jpeg", 0)

# Threshold untuk mendapatkan citra biner
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Buat structuring element
kernel = np.ones((5,5), np.uint8)

# Lakukan erosi
eroded = cv2.erode(binary, kernel, iterations=1)

# Tampilkan perbandingan
comparison = np.hstack((binary, eroded))

cv2.imshow("Binary | Erosion (5x5)", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Insight Engineering

Erosi digunakan ketika:

- Menghilangkan noise kecil setelah threshold
- Memisahkan objek yang saling bersentuhan tipis
- Mengurangi ketebalan garis sebelum skeletonization

Namun berisiko:

- Menghilangkan objek kecil penting
- Mengubah struktur tipis

---

# 3.5.3 Dilasi (Dilation)

## Definisi Matematis

$$
A \oplus B = \{ z \mid (B̂)_z \cap A \neq \emptyset \}
$$

Artinya:
Suatu piksel menjadi bagian objek jika **ada minimal satu piksel kernel yang bertumpukan dengan objek**.

---

## Interpretasi Geometris

Jika erosi adalah penyusutan, maka dilasi adalah ekspansi.

Secara visual:

- Celah kecil tertutup
- Lubang kecil terisi
- Objek tipis menjadi lebih tebal

Dilasi dapat meningkatkan konektivitas antar objek.

---

## Dampak Topologis

Dilasi dapat:

- Menggabungkan dua objek yang berdekatan
- Menambah luas objek
- Mengubah perimeter

---

## Implementasi

```
cv2.dilate(src, kernel, iterations)
```

---

## Contoh — Dilasi

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

kernel = np.ones((5,5), np.uint8)

dilated = cv2.dilate(binary, kernel, iterations=1)

comparison = np.hstack((binary, dilated))

cv2.imshow("Binary | Dilation (5x5)", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Insight Engineering

Digunakan untuk:

- Mengisi gap pada karakter OCR
- Menyambungkan jalur retak (crack detection)
- Menguatkan struktur sebelum contour detection

Risiko:

- Noise ikut membesar
- Over-merging objek

---

# 3.5.4 Opening dan Closing

Opening dan closing adalah kombinasi operator dasar.

---

## Opening

$$
A \circ B = (A \ominus B) \oplus B
$$

Proses:
1. Erosi → hilangkan detail kecil
2. Dilasi → kembalikan ukuran utama objek

Fungsi utama:
- Menghapus noise kecil
- Mempertahankan bentuk global

---

## Closing

$$
A \bullet B = (A \oplus B) \ominus B
$$

Proses:
1. Dilasi → isi celah
2. Erosi → kembalikan ukuran utama

Fungsi utama:
- Menutup lubang kecil
- Menghubungkan celah tipis

---

## Contoh — Opening vs Closing

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

kernel = np.ones((5,5), np.uint8)

opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

comparison = np.hstack((binary, opening, closing))

cv2.imshow("Binary | Opening | Closing", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Analisis Engineering

Opening cocok untuk:
- Noise titik kecil (salt noise)

Closing cocok untuk:
- Lubang kecil pada objek solid
- Retakan tipis pada komponen

---

# 3.5.5 Morphological Gradient

## Definisi

$$
Gradient = (A \oplus B) - (A \ominus B)
$$

Artinya:
Selisih antara ekspansi dan penyusutan objek.

---

## Interpretasi

Gradient menyoroti batas luar objek.

Berbeda dengan Sobel:
- Sobel berbasis turunan intensitas
- Morphological gradient berbasis struktur bentuk

---

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

kernel = np.ones((3,3), np.uint8)

gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

comparison = np.hstack((binary, gradient))

cv2.imshow("Binary | Morphological Gradient", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Kapan Digunakan?

- Deteksi batas objek industri
- Preprocessing contour detection
- Ekstraksi outline objek

---

# 3.5.6 Top Hat dan Black Hat

## Top Hat

$$
TopHat = A - (A \circ B)
$$

Menyoroti objek kecil terang yang lebih kecil dari kernel.

---

## Black Hat

$$
BlackHat = (A \bullet B) - A
$$

Menyoroti objek kecil gelap.

---

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg", 0)

kernel = np.ones((15,15), np.uint8)

tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

comparison = np.hstack((img, tophat, blackhat))

cv2.imshow("Original | TopHat | BlackHat", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Insight Engineering

TopHat sering digunakan untuk:
- Menonjolkan teks pada background terang
- Preprocessing plat nomor

BlackHat digunakan untuk:
- Retakan gelap pada logam
- Cacat kecil pada permukaan

---

# 3.5.7 Studi Kasus Teknik

Pada sistem nyata, morfologi hampir tidak pernah berdiri sendiri.  
Ia bekerja sebagai bagian dari pipeline yang dirancang untuk:

- Menstabilkan segmentasi
- Memperbaiki struktur objek
- Mengontrol topologi hasil threshold

Di bawah ini kita analisis secara teknis mengapa setiap langkah digunakan.

---

## Kasus 1 — Inspeksi Komponen Industri

### Permasalahan Lapangan

Dalam inspeksi komponen logam atau PCB:

- Noise muncul akibat refleksi cahaya
- Permukaan memiliki tekstur mikro
- Terdapat lubang kecil atau celah solder
- Objek cacat bisa sangat kecil

Histogram sering tidak ideal, sehingga hasil threshold masih mengandung noise granular.

---

### Pipeline

1. Gaussian Blur  
2. Otsu Threshold  
3. Opening  
4. Closing  

```python
import cv2
import numpy as np

# 1. Baca citra grayscale
img = cv2.imread("anu.jpeg", 0)

# 2. Gaussian Blur untuk reduksi noise frekuensi tinggi
blur = cv2.GaussianBlur(img, (5,5), 0)

# 3. Otsu threshold
_, thresh = cv2.threshold(
    blur, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# 4. Structuring element
kernel = np.ones((5,5), np.uint8)

# 5. Opening (hapus noise kecil)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# 6. Closing (tutup celah kecil)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

# 7. Tampilkan bersandingan
comparison = np.hstack((thresh, opening, closing))

cv2.imshow("Threshold | Opening | Closing", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### Pemaknaan Engineering

• Gaussian Blur → mengurangi noise frekuensi tinggi  
• Otsu → memilih threshold optimal berbasis histogram  
• Opening → menghapus noise kecil yang lolos threshold  
• Closing → menutup celah kecil pada objek utama  

Secara topologis:

- Opening mengurangi jumlah komponen kecil
- Closing meningkatkan konektivitas internal objek

Tujuan akhir:
Menstabilkan bentuk sebelum analisis kontur atau pengukuran dimensi.

Jika tahap ini dilewati, contour detection dapat menghasilkan:

- False defect
- Over-segmentation
- Penghitungan objek salah

---

## Kasus 2 — Deteksi Plat Nomor

### Permasalahan Lapangan

- Background tidak homogen
- Teks relatif kecil dibandingkan area citra
- Kontras karakter tidak selalu ekstrem
- Bayangan kendaraan

---

### Strategi

TopHat → tonjolkan karakter terang  
Threshold → segmentasi  
Closing → hubungkan stroke karakter  

```python
import cv2
import numpy as np

# 1. Baca citra grayscale
img = cv2.imread("anu.jpeg", 0)

# 2. Structuring element
kernel = np.ones((15,15), np.uint8)

# 3. TopHat untuk menonjolkan karakter terang kecil
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# 4. Otsu threshold
_, thresh = cv2.threshold(
    tophat, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# 5. Closing untuk menghubungkan stroke karakter
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# 6. Tampilkan bersandingan
comparison = np.hstack((tophat, thresh, closing))

cv2.imshow("TopHat | Threshold | Closing", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### Pemaknaan Engineering

TopHat secara matematis:

$$
TopHat = A - (A \circ B)
$$

Artinya:
Menonjolkan struktur kecil terang yang lebih kecil dari kernel.

Dalam konteks plat nomor:

- Karakter huruf relatif kecil
- Background lebih luas

TopHat meningkatkan separability lokal sebelum threshold.

Closing kemudian:

- Menghubungkan stroke huruf
- Mengurangi fragmentasi karakter

Tujuan akhir:
Menghasilkan region kandidat sebelum OCR atau contour filtering berbasis aspect ratio.

Tanpa morfologi:
- Karakter bisa terputus
- OCR gagal membaca

---

## Kasus 3 — Segmentasi Sel Mikroskop

### Permasalahan Lapangan

- Noise granular
- Sel saling menempel
- Background tidak rata
- Kontras rendah

---

### Pipeline

Adaptive Threshold → Opening  

```python
import cv2
import numpy as np

# 1. Baca citra grayscale
img = cv2.imread("anu.jpeg", 0)

# 2. Adaptive threshold
adaptive = cv2.adaptiveThreshold(
    img,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    11,
    2
)

# 3. Structuring element kecil
kernel = np.ones((3,3), np.uint8)

# 4. Opening untuk hapus noise kecil
opening = cv2.morphologyEx(adaptive, cv2.MORPH_OPEN, kernel)

# 5. Tampilkan bersandingan
comparison = np.hstack((adaptive, opening))

cv2.imshow("Adaptive | Opening", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### Pemaknaan Engineering

Adaptive threshold memperhitungkan variasi pencahayaan lokal.

Opening digunakan untuk:

- Menghapus noise kecil
- Memisahkan sel yang hanya bersentuhan tipis

Namun perlu diperhatikan:

Kernel terlalu besar → sel kecil hilang  
Kernel terlalu kecil → noise tidak hilang  

Dalam pipeline lanjutan, hasil ini sering digunakan untuk:

- Distance transform
- Watershed segmentation
- Perhitungan jumlah sel

---

# Analisis Engineering Mendalam

## 1. Dampak Kernel Size terhadap Topologi

Kernel dapat dianggap sebagai operator skala.

Jika ukuran kernel = k:

- Objek lebih kecil dari k akan hilang (pada opening)
- Lubang lebih kecil dari k akan tertutup (pada closing)

Secara konseptual:

Kernel adalah parameter resolusi morfologis.

---

## 2. Dampak Kernel terhadap Konektivitas

Dalam citra biner, objek memiliki konektivitas:

- 4-connected
- 8-connected

Morfologi dapat:

- Memutus konektivitas
- Menyatukan konektivitas

Hal ini berdampak pada:

- Jumlah komponen terhubung
- Hasil contour detection
- Perhitungan luas dan perimeter

---

## 3. Bentuk Kernel dan Implikasinya

```python
rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
```

### Rectangular

- Agresif
- Mengubah sudut menjadi lebih kotak
- Cocok untuk objek industri buatan manusia

### Ellipse

- Lebih isotropik
- Cocok untuk struktur biologis
- Minim distorsi bentuk alami

### Cross

- Mempertahankan struktur tipis vertikal/horizontal
- Tidak terlalu agresif pada diagonal

---

## 4. Trade-Off Desain Sistem

Dalam sistem nyata selalu ada kompromi:

| Tujuan | Risiko |
|--------|--------|
| Hapus noise | Hilangkan detail kecil |
| Tutup celah | Gabungkan objek terpisah |
| Stabilkan bentuk | Distorsi geometri |

Morfologi adalah alat kontrol struktur, bukan sekadar filter visual.

---

# Kesimpulan Engineering

Pada level sistem:

- Threshold menghasilkan klasifikasi piksel
- Morfologi mengatur struktur dan topologi
- Contour detection menganalisis bentuk
- Feature extraction menghitung parameter geometris

Tanpa morfologi yang tepat:

- Sistem akan tidak stabil
- False positive meningkat
- Evaluasi kuantitatif (IoU, precision) menurun

Morfologi adalah jembatan antara segmentasi dan analisis bentuk.


# Ringkasan Bab 3.5

1. Morfologi berbasis teori himpunan.
2. Erosi mengecilkan objek.
3. Dilasi memperbesar objek.
4. Opening menghapus noise kecil.
5. Closing menutup lubang kecil.
6. Gradient menyoroti batas.
7. TopHat & BlackHat menyoroti detail kecil.
8. Kernel menentukan hasil.
9. Pipeline lebih penting dari satu operasi.
10. Morfologi penting dalam segmentasi lanjutan.

---

# Ide Mini Project

1. Inspeksi kualitas solder PCB.
2. Penghitungan sel otomatis.
3. Deteksi karakter plat nomor.
4. Analisis pengaruh kernel terhadap IoU.
5. Visualisasi perubahan objek per iterasi.
6. Pipeline morfologi adaptif.
7. Evaluasi presisi segmentasi.
8. Integrasi morfologi + contour detection.
9. Sistem penghapus noise otomatis.
10. Studi eksperimen bentuk kernel terhadap akurasi.