# 3.6 Deteksi Tepi (Edge Detection)

---

## 1. Pendahuluan

Deteksi tepi (edge detection) merupakan salah satu operasi fundamental dalam pengolahan citra digital yang bertujuan mengekstraksi batas objek berdasarkan diskontinuitas intensitas. Dalam konteks pipeline computer vision, edge detection berfungsi sebagai tahap transisi antara low-level processing (filtering, smoothing, morfologi) menuju mid-level processing seperti contour extraction, shape analysis, dan feature detection.

Secara konseptual, tepi adalah lokasi di mana terjadi perubahan signifikan pada fungsi intensitas citra.

Jika citra didefinisikan sebagai fungsi diskret dua dimensi:

$$
I : \mathbb{Z}^2 \rightarrow \mathbb{R}
$$

dengan:

- $(x, y) \in \mathbb{Z}^2$ adalah koordinat piksel  
- $I(x,y)$ adalah intensitas piksel  

Maka tepi adalah himpunan titik yang memenuhi kondisi:

$$
|\nabla I(x,y)| \geq T
$$

dengan:

- $\nabla I$ adalah gradien citra  
- $T$ adalah ambang batas  

---

## 2. Formulasi Matematis Gradien

Gradien citra didefinisikan sebagai:

$$
\nabla I =
\begin{bmatrix}
\frac{\partial I}{\partial x} \\
\frac{\partial I}{\partial y}
\end{bmatrix}
$$

Magnitudo gradien:

$$
|\nabla I| = \sqrt{\left(\frac{\partial I}{\partial x}\right)^2 + \left(\frac{\partial I}{\partial y}\right)^2}
$$

Orientasi gradien:

$$
\theta = \tan^{-1} \left( \frac{\partial I / \partial y}{\partial I / \partial x} \right)
$$

Interpretasi matematis:

- Gradien menunjukkan arah perubahan maksimum.
- Besarnya gradien menunjukkan tingkat kontras lokal.

Interpretasi engineering:

- Nilai tinggi → kemungkinan batas objek.
- Nilai rendah → area homogen.

---

## 3. Diskretisasi Turunan

Karena citra bersifat diskret, turunan dihitung menggunakan konvolusi kernel:

$$
\frac{\partial I}{\partial x} \approx I * K_x
$$

$$
\frac{\partial I}{\partial y} \approx I * K_y
$$

Konvolusi dua dimensi:

$$
(I * K)(x,y) =
\sum_{i=-k}^{k}
\sum_{j=-k}^{k}
I(x-i,y-j)K(i,j)
$$

Kompleksitas komputasi:

$$
O(N \cdot k^2)
$$

dengan:

- $N$ jumlah piksel  
- $k$ ukuran kernel  

---

## 4. Operator Sobel

Kernel Sobel:

$$
K_x =
\begin{bmatrix}
-1 & 0 & 1 \\
-2 & 0 & 2 \\
-1 & 0 & 1
\end{bmatrix}
$$

$$
K_y =
\begin{bmatrix}
-1 & -2 & -1 \\
0 & 0 & 0 \\
1 & 2 & 1
\end{bmatrix}
$$

Sobel menggabungkan smoothing horizontal/vertikal dan diferensiasi.

### Implementasi Sobel

```python
import cv2
import numpy as np

img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

magnitude = cv2.magnitude(sobelx, sobely)
magnitude = np.uint8(np.absolute(magnitude))

comparison = np.hstack((gray, magnitude))

cv2.imshow("Sobel Edge Detection", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Parameter penting:

- `ddepth` menentukan tipe output.
- `ksize` mempengaruhi sensitivitas dan smoothing.
- Kernel lebih besar → lebih halus, tetapi detail halus hilang.

---

## 5. Operator Laplacian

Turunan orde kedua:

$$
\nabla^2 I =
\frac{\partial^2 I}{\partial x^2} +
\frac{\partial^2 I}{\partial y^2}
$$

Kernel umum:

$$
\begin{bmatrix}
0 & 1 & 0 \\
1 & -4 & 1 \\
0 & 1 & 0
\end{bmatrix}
$$

Laplacian memperkuat noise sehingga biasanya didahului smoothing.

### Implementasi Laplacian

```python
import cv2
import numpy as np

img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

lap = cv2.Laplacian(gray, cv2.CV_64F)
lap = np.uint8(np.absolute(lap))

comparison = np.hstack((gray, lap))

cv2.imshow("Laplacian Edge Detection", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 6. Canny Edge Detection

Canny adalah algoritma optimal berdasarkan tiga kriteria:

1. Good detection  
2. Good localization  
3. Single response  

Tahapan:

1. Gaussian smoothing
2. Perhitungan gradien
3. Non-maximum suppression
4. Double threshold
5. Hysteresis tracking

Gaussian filter:

$$
G(x,y) =
\frac{1}{2\pi\sigma^2}
e^{-\frac{x^2+y^2}{2\sigma^2}}
$$

### Implementasi Canny

```python
import cv2
import numpy as np

img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5,5), 1.4)

edges = cv2.Canny(blur, 50, 150)

comparison = np.hstack((gray, edges))

cv2.imshow("Canny Edge Detection", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Parameter:

- `threshold1` ambang bawah
- `threshold2` ambang atas
- Rasio umum: 1:2 atau 1:3

---

## 7. Studi Kasus 1 — Deteksi Retak Beton

Pipeline:

Grayscale → Gaussian → Canny → Closing

```python
import cv2
import numpy as np

img = cv2.imread('crack.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5,5), 1.5)
edges = cv2.Canny(blur, 30, 100)

kernel = np.ones((3,3), np.uint8)
closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

comparison = np.hstack((gray, closing))

cv2.imshow("Concrete Crack Detection", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Analisis:

- Threshold rendah untuk mendeteksi retak tipis.
- Closing menjaga konektivitas.

---

## 8. Studi Kasus 2 — Deteksi Marka Jalan (Lane Detection)

### Permasalahan Lapangan

Pada sistem Advanced Driver Assistance Systems (ADAS), deteksi marka jalan digunakan untuk:

- Menentukan posisi kendaraan relatif terhadap jalur
- Memberikan peringatan lane departure
- Mendukung sistem autonomous steering

Tantangan utama:

- Noise akibat bayangan
- Perubahan iluminasi
- Marka pudar
- Garis terputus
- Perspektif kamera

Marka jalan secara geometris dapat dimodelkan sebagai garis lurus dalam domain citra (untuk area ROI terbatas), sehingga cocok dianalisis menggunakan Transformasi Hough.

---

### Pipeline Sistem

1. Konversi ke grayscale  
2. Gaussian smoothing  
3. Canny edge detection  
4. Region of Interest (ROI masking)  
5. Hough Line Transform  

Pipeline lengkap:

$$
I(x,y)
\rightarrow
\text{Gaussian}
\rightarrow
\nabla I
\rightarrow
\text{Canny}
\rightarrow
\text{Hough}
$$

---

### Formulasi Matematis Hough Transform

Persamaan garis dalam bentuk polar:

$$
\rho = x \cos\theta + y \sin\theta
$$

dengan:

- $\rho$ = jarak garis terhadap origin  
- $\theta$ = sudut normal garis  
- $(x,y)$ = koordinat piksel edge  

Setiap piksel edge memberikan kurva sinusoidal pada ruang parameter $(\rho, \theta)$. Titik potong maksimum pada accumulator menunjukkan keberadaan garis.

Kompleksitas komputasi:

Jika jumlah piksel edge = $M$ dan resolusi parameter sudut = $T$:

$$
O(M \cdot T)
$$

---

### Implementasi Lengkap (Self-Contained)

```python
import cv2
import numpy as np

# 1. Baca citra
img = cv2.imread('lane.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Gaussian Blur
blur = cv2.GaussianBlur(gray, (5,5), 1.5)

# 3. Canny Edge
edges = cv2.Canny(blur, 50, 150)

# 4. Region of Interest (mask segitiga)
height, width = edges.shape
mask = np.zeros_like(edges)

roi_corners = np.array([[
    (0, height),
    (width//2, height//2),
    (width, height)
]], dtype=np.int32)

cv2.fillPoly(mask, roi_corners, 255)
roi_edges = cv2.bitwise_and(edges, mask)

# 5. Hough Line Transform
lines = cv2.HoughLinesP(
    roi_edges,
    rho=1,
    theta=np.pi/180,
    threshold=100,
    minLineLength=50,
    maxLineGap=20
)

# 6. Gambar garis pada salinan citra
line_img = img.copy()

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_img, (x1,y1), (x2,y2), (0,255,0), 3)

# 7. Visualisasi
comparison = np.hstack((gray, roi_edges))
cv2.imshow("Lane Detection - Gray vs ROI Edge", comparison)
cv2.imshow("Detected Lanes", line_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### Penjelasan Parameter `cv2.HoughLinesP`

```
cv2.HoughLinesP(image, rho, theta, threshold, minLineLength, maxLineGap)
```

- `rho` : resolusi jarak dalam piksel  
- `theta` : resolusi sudut dalam radian  
- `threshold` : minimum vote accumulator  
- `minLineLength` : panjang garis minimum  
- `maxLineGap` : jarak maksimum antar segmen yang masih dianggap satu garis  

---

### Analisis Engineering

#### 1. Sensitivitas Threshold Canny

Jika terlalu rendah:
- Noise masuk ke Hough
- False positive garis meningkat

Jika terlalu tinggi:
- Garis terputus
- Vote accumulator rendah

#### 2. Sensitivitas Parameter Hough

- `threshold` terlalu tinggi → garis tidak terdeteksi
- `minLineLength` terlalu besar → marka pendek hilang
- `maxLineGap` terlalu kecil → garis terfragmentasi

#### 3. Trade-off Desain

$$
\text{Detection Robustness}
\leftrightarrow
\text{False Positive Suppression}
$$

#### 4. Dampak pada Tahap Lanjutan

- Lane curvature estimation
- Vehicle position estimation
- Tracking stabilitas temporal

Jika edge tidak stabil → lane estimation jitter.

---

### Evaluasi Sistem

Metode evaluasi kuantitatif:

- Precision & Recall terhadap ground truth
- Mean deviation garis terhadap anotasi manual
- Frame processing time (FPS)

---

### Kesimpulan Kasus

Edge detection berfungsi sebagai fondasi untuk transformasi parametrik seperti Hough. Stabilitas edge menentukan kestabilan garis yang terdeteksi. Dalam sistem kendaraan otonom, tuning parameter harus dilakukan berdasarkan kondisi pencahayaan dan resolusi kamera.


---

# 9. Analisis Engineering Lanjutan

## 9.1 Model Noise dan Amplifikasi Gradien

Misalkan citra teramati mengandung noise aditif:

$$
I_n(x,y) = I(x,y) + n(x,y)
$$

dengan:

- $I(x,y)$ : citra ideal  
- $n(x,y)$ : noise acak dengan distribusi Gaussian  
- $n(x,y) \sim \mathcal{N}(0, \sigma_n^2)$  
- $\sigma_n^2$ : variansi noise  

Ketika dilakukan operasi turunan pertama:

$$
\nabla I_n = \nabla I + \nabla n
$$

Karena turunan merupakan operator high-pass filter, maka komponen noise frekuensi tinggi diperkuat.

Variansi gradien noise menjadi:

$$
\mathrm{Var}(\nabla n) \propto \sigma_n^2 \cdot \|K\|^2
$$

dengan:

- $K$ adalah kernel diferensial (misalnya Sobel)
- $\|K\|^2$ adalah energi kernel

Interpretasi engineering:

- Semakin besar noise awal ($\sigma_n^2$), semakin besar false edge.
- Operator diferensial memperbesar noise frekuensi tinggi.
- Tanpa smoothing, sistem menjadi tidak stabil.

---

## 9.2 Peran Gaussian Smoothing terhadap Variansi

Gaussian filter:

$$
G(x,y) =
\frac{1}{2\pi\sigma^2}
e^{-\frac{x^2+y^2}{2\sigma^2}}
$$

merupakan low-pass filter dengan respon frekuensi:

$$
H(f) = e^{-2\pi^2 \sigma^2 f^2}
$$

Jika noise bersifat white noise, maka setelah Gaussian smoothing:

$$
\sigma_{n,filtered}^2 < \sigma_n^2
$$

Namun trade-off terjadi:

- $\sigma$ kecil → detail tajam, noise masih besar
- $\sigma$ besar → noise turun, edge melebar

Trade-off matematis:

$$
\text{Noise Reduction} \leftrightarrow \text{Edge Localization Accuracy}
$$

Jika $\sigma$ terlalu besar, lokasi tepi bergeser (bias posisi).

---

## 9.3 Sensitivitas Threshold pada Canny

Canny menggunakan dua ambang:

- $T_{low}$
- $T_{high}$

Secara empiris:

$$
T_{high} \approx 2T_{low} \text{ hingga } 3T_{low}
$$

Jika:

$$
T_{low} \ll |\nabla I|
$$

maka banyak noise lolos.

Jika:

$$
T_{high} \gg |\nabla I|
$$

maka edge tipis hilang.

Dampak sistemik:

- Threshold rendah → banyak komponen topologi kecil
- Threshold tinggi → fragmentasi edge

---

## 9.4 Dampak terhadap Topologi Objek

Edge membentuk graf konektivitas piksel.

Jika kita definisikan:

- $C$ = jumlah connected components
- $H$ = jumlah hole

Maka karakteristik topologi (Euler characteristic):

$$
\chi = C - H
$$

Kesalahan threshold menyebabkan:

- Fragmentasi → $C$ meningkat
- False hole → $H$ meningkat
- $\chi$ berubah drastis

Implikasi pada contour detection:

- Banyak contour kecil tak relevan
- Shape descriptor tidak stabil
- Momen Hu berubah signifikan

---

## 9.5 Trade-off Presisi vs Robustness

Secara sistem:

- Presisi tinggi → threshold rendah → sensitif noise
- Robustness tinggi → threshold tinggi → detail hilang

Dinyatakan sebagai optimisasi:

$$
\min_{T,\sigma}
\left(
\alpha \cdot \text{False Positive}
+
\beta \cdot \text{Missed Edge}
\right)
$$

dengan:

- $\alpha, \beta$ bobot desain sistem

Pada sistem kendaraan otonom, false positive dapat menyebabkan deteksi marka palsu.
Pada OCR, missed edge menyebabkan huruf tidak terbaca.

---

# 10. Kompleksitas Komputasi Detail

Misalkan ukuran citra $M \times N$ sehingga jumlah piksel:

$$
P = M \cdot N
$$

## 10.1 Sobel

Konvolusi kernel $k \times k$:

$$
O(P \cdot k^2)
$$

Untuk $k=3$:

- Operasi konstan ≈ 9 multiplikasi per piksel
- Relatif ringan untuk real-time

## 10.2 Canny

Tahapan dan kompleksitas:

1. Gaussian blur → $O(P \cdot k^2)$  
2. Gradient computation → $O(P)$  
3. Non-maximum suppression → $O(P)$  
4. Double threshold → $O(P)$  
5. Hysteresis tracking → worst-case $O(P)$  

Total:

$$
O(P \cdot k^2 + 4P)
$$

Secara teoritis tetap linear, namun konstanta komputasi jauh lebih besar.

Implikasi engineering:

- Pada resolusi 1920×1080:
  - Sobel jauh lebih cepat
  - Canny membutuhkan optimasi (ROI, downsampling)

---

## 10.3 Cache dan Memory Access

Konvolusi membutuhkan akses memori lokal tetangga piksel.

Faktor performa nyata:

- Cache locality
- SIMD optimization
- GPU acceleration

Pada embedded system tanpa GPU:

- Kernel kecil lebih stabil
- Hindari sigma besar

---

# 11. Keterkaitan Sistemik dalam Pipeline Computer Vision

## 11.1 Setelah Morfologi

Morfologi memperbaiki struktur biner.

Edge detection:

- Menghasilkan boundary presisi
- Menentukan batas kontur

Jika morfologi terlalu agresif:
- Edge menjadi terlalu halus
- Detail hilang

---

## 11.2 Dampak terhadap Contour Detection

Contour extraction bergantung pada edge tertutup.

Jika edge terfragmentasi:

- Banyak contour kecil
- Area dan perimeter bias
- Bounding box tidak akurat

Jika edge terlalu tebal:

- Perimeter meningkat
- Shape descriptor bias

---

## 11.3 Dampak terhadap Tracking

Tracking berbasis centroid:

$$
(x_c, y_c) =
\left(
\frac{1}{A}\sum x,
\frac{1}{A}\sum y
\right)
$$

Jika edge tidak stabil:

- Area $A$ berubah-ubah
- Centroid jitter
- Tracking tidak stabil

---

## 11.4 Dampak terhadap OCR

Huruf terdiri dari stroke tipis.

Jika threshold tinggi:

- Stroke hilang
- Karakter terputus

Jika threshold rendah:

- Noise menyatu dengan huruf
- False region muncul

---

## 11.5 Dampak terhadap Hough Transform

Hough membutuhkan edge kontinu.

Jika edge noisy:

- Accumulator penuh noise
- False line detection

Jika edge terlalu jarang:

- Vote tidak cukup
- Garis gagal terdeteksi

---

# Kesimpulan Engineering Mendalam

Deteksi tepi bukan sekadar operator diferensial.

Ia adalah modul kritikal yang:

- Memperkuat noise
- Mengubah struktur topologi objek
- Mempengaruhi stabilitas contour
- Mempengaruhi estimasi bentuk
- Menentukan kestabilan tracking
- Mempengaruhi akurasi OCR
- Mempengaruhi transformasi parametrik seperti Hough

Desain sistem edge detection harus mempertimbangkan:

- Distribusi noise
- Variansi
- Kompleksitas komputasi
- Kebutuhan real-time
- Tahap lanjutan dalam pipeline

Kesalahan tuning bukan hanya menghasilkan gambar buruk,
tetapi menyebabkan kegagalan sistem secara keseluruhan.


---

## 12. Ringkasan Engineering

Deteksi tepi adalah modul diferensial yang secara eksplisit memperbesar komponen frekuensi tinggi pada citra. Secara matematis, operator gradien bertindak sebagai high-pass filter sehingga setiap komponen noise dengan variansi $\sigma_n^2$ akan mengalami amplifikasi proporsional terhadap energi kernel diferensial. Artinya, kualitas edge tidak hanya bergantung pada struktur objek, tetapi juga pada model noise sistem akuisisi.

Dalam desain sistem vision nyata, terdapat tiga variabel dominan yang saling berinteraksi:

1. **Tingkat noise sensor ($\sigma_n^2$)**
2. **Parameter smoothing ($\sigma$ Gaussian, ukuran kernel)**
3. **Ambang deteksi (threshold Canny atau magnitudo gradien minimum)**

Relasi fundamentalnya dapat diringkas sebagai:

$$
\text{Stabilitas Edge} =
f(\sigma_n^2, \sigma_{Gaussian}, T)
$$

Jika smoothing terlalu kecil:
- Noise diperkuat oleh turunan
- False positive meningkat
- Topologi objek terfragmentasi

Jika smoothing terlalu besar:
- Edge melebar
- Lokalisasi bergeser (bias posisi)
- Detail kecil hilang

Jika threshold terlalu rendah:
- Banyak komponen kecil terbentuk
- Kontur tidak relevan meningkat
- Beban komputasi tahap lanjutan bertambah

Jika threshold terlalu tinggi:
- Edge tipis hilang
- Kontur tidak tertutup
- Hough transform dan tracking gagal

Secara sistemik, deteksi tepi mempengaruhi seluruh pipeline:

- **Contour detection** → membutuhkan edge tertutup dan kontinu  
- **Shape descriptor** → sensitif terhadap perubahan perimeter  
- **Tracking** → bergantung pada stabilitas area dan centroid  
- **OCR** → memerlukan preservasi stroke tipis  
- **Hough transform** → memerlukan edge kuat dan terstruktur  

Dari perspektif komputasi, edge detection adalah operasi linear terhadap jumlah piksel, tetapi konstanta waktu bergantung pada ukuran kernel dan jumlah tahapan (khususnya pada Canny). Pada sistem real-time beresolusi tinggi, strategi seperti ROI selection, downsampling, dan optimasi hardware menjadi krusial.

Secara keseluruhan, deteksi tepi bukan sekadar tahap visualisasi batas objek, melainkan komponen struktural dalam arsitektur sistem computer vision. Parameter yang tidak dituning dengan benar dapat menyebabkan instabilitas topologi, bias geometris, dan kegagalan pada tahap analisis lanjutan. Oleh karena itu, perancangan edge detection harus dilakukan berdasarkan karakteristik noise, kebutuhan presisi geometris, serta batasan komputasi sistem target.

---

## 13. Mini Project Lanjutan

1. Evaluasi pengaruh sigma terhadap stabilitas edge.
2. Bandingkan Sobel dan Canny pada citra noisy.
3. Analisis fragmentasi contour akibat threshold rendah.
4. Integrasi edge dengan contour measurement.
5. Optimasi edge detection untuk sistem real-time.
6. Evaluasi dampak resolusi terhadap performa.
7. Edge-based dimension estimation.
8. Adaptive Canny thresholding.
9. Analisis respon frekuensi Sobel.
10. Integrasi edge detection dengan homography.

---