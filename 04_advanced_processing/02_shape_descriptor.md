# 4.2  Shape Descriptor (Deskriptor Bentuk)

---

# 1. Posisi Shape Descriptor dalam Pipeline Computer Vision

Pipeline sistem visi klasik:

Akuisisi → Preprocessing → Segmentasi → Kontur → Shape Descriptor → Decision System

Setelah objek berhasil dipisahkan dari latar belakang, sistem tidak lagi bekerja pada matriks piksel mentah, melainkan pada representasi geometri yang lebih ringkas.

Objek biner:

$$
\Omega = \{(x,y) \in \mathbb{Z}^2 \mid I(x,y) = 1 \}
$$

Shape descriptor:

$$
D(\Omega) = \mathbf{f} \in \mathbb{R}^k
$$

Interpretasi:

- $\Omega$ → domain spasial
- $\mathbf{f}$ → ruang fitur berdimensi rendah
- $k$ → jumlah parameter bentuk

Reduksi dimensi:

$$
\mathbb{R}^{262144} \rightarrow \mathbb{R}^{7}
$$

(Contoh citra 512×512 ke 7 Hu moments)

---

# 2. Dasar Matematis dan Intuisi Teknik

## 2.1 Momen dan Distribusi Massa

Momen orde nol:

$$
m_{00} = \sum_x \sum_y I(x,y)
$$

→ Luas objek

Momen orde pertama:

$$
m_{10}, m_{01}
$$

Centroid:

$$
\bar{x} = \frac{m_{10}}{m_{00}}, \quad
\bar{y} = \frac{m_{01}}{m_{00}}
$$

Interpretasi:

Centroid adalah titik keseimbangan geometris.

---

## 2.2 Perimeter

$$
P = \sum_{i=1}^{N} \|\mathbf{p}_{i+1} - \mathbf{p}_i\|
$$

Kompleksitas: $O(N)$.

---

## 2.3 Circularity

$$
C = \frac{4\pi A}{P^2}
$$

Lingkaran → nilai maksimum.

Noise kecil → perimeter naik → circularity turun drastis.

---

## 2.4 Hu Moments

Momen terpusat:

$$
\mu_{pq} = \sum (x-\bar{x})^p (y-\bar{y})^q I(x,y)
$$

Invarian terhadap:

- Translasi
- Rotasi
- Skala

Normalisasi:

$$
H_i' = -\text{sign}(H_i)\log_{10}|H_i|
$$

---

## 2.5 Convex Hull dan Solidity

$$
\text{Solidity} = \frac{A}{A_{convex}}
$$

Kompleksitas convex hull: $O(N \log N)$.

---

# 3. IMPLEMENTASI OPENCV

Fungsi:

- cv2.contourArea()
- cv2.arcLength()
- cv2.moments()
- cv2.HuMoments()
- cv2.convexHull()

Flag findContours:

- RETR_EXTERNAL
- CHAIN_APPROX_SIMPLE

---

# STUDI KASUS 1  
## Quality Control Industri — Circularity

Permasalahan: Tutup botol harus bulat sempurna.

```python
import cv2
import numpy as np

img = cv2.imread("bottle_cap.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

annotated = img.copy()

for cnt in contours:
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)

    if perimeter == 0:
        continue

    circularity = 4*np.pi*area/(perimeter**2)

    x,y,w,h = cv2.boundingRect(cnt)

    if circularity < 0.85:
        cv2.rectangle(annotated,(x,y),(x+w,y+h),(0,0,255),2)
    else:
        cv2.rectangle(annotated,(x,y),(x+w,y+h),(0,255,0),2)

comparison = np.hstack((img, annotated))

cv2.imshow("Before vs After QC", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Analisis:

Threshold rendah → noise tepi meningkat → perimeter meningkat → circularity menurun → terjadi false reject pada produk yang sebenarnya masih layak.

Secara matematis, perimeter berada pada penyebut kuadrat dalam rumus circularity:

C = 4πA / P²

Kenaikan kecil pada P akan memberikan penurunan signifikan pada C. Oleh karena itu, sistem inspeksi industri wajib memastikan segmentasi stabil sebelum ekstraksi fitur.

---

# STUDI KASUS 2  
## OCR — Hu Moments (Before–After)

### Permasalahan

Membedakan angka 0 dan 1 meskipun mengalami rotasi, translasi, atau perubahan skala kecil pada proses akuisisi citra.

### Pipeline

Grayscale → Threshold Invers → Ekstraksi Kontur → Perhitungan Hu Moments → Klasifikasi Sederhana

```python
import cv2
import numpy as np

img = cv2.imread("digit.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

annotated = img.copy()

for cnt in contours:
    moments = cv2.moments(cnt)
    hu = cv2.HuMoments(moments)

    for i in range(7):
        hu[i] = -np.sign(hu[i]) * np.log10(abs(hu[i]) + 1e-10)

    x, y, w, h = cv2.boundingRect(cnt)

    if hu[0] > 0.5:
        label = "0"
    else:
        label = "1"

    cv2.putText(
        annotated,
        label,
        (x, y-5),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

comparison = np.hstack((img, annotated))

cv2.imshow("Before vs After OCR", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Analisis Engineering

Hu Moments bersifat invarian terhadap translasi, rotasi, dan skala karena dibangun dari momen terpusat dan dinormalisasi. Secara sistem, ini membuat fitur tetap stabil meskipun objek diputar atau dipindahkan.

Namun, descriptor ini sangat sensitif terhadap perubahan topologi akibat kesalahan segmentasi. Jika threshold terlalu agresif:

- Lubang internal pada angka 0 bisa tertutup.
- Noise kecil dapat menempel pada batas objek.
- Distribusi massa berubah signifikan.

Perubahan kecil tersebut mengubah nilai momen hingga orde tinggi, sehingga memengaruhi hasil klasifikasi.

Kompleksitas komputasi tetap O(N) terhadap jumlah piksel kontur, sehingga masih layak untuk sistem real-time ringan.

---

# STUDI KASUS 3  
## Analisis Medis — Solidity (Before–After)

### Permasalahan

Sel abnormal pada citra mikroskopis sering memiliki cekungan tidak wajar. Tujuan sistem adalah mengidentifikasi sel dengan bentuk tidak konveks secara signifikan.

### Pipeline

Grayscale → Threshold → Kontur → Convex Hull → Perhitungan Solidity → Penandaan

```python
import cv2
import numpy as np

img = cv2.imread("cell.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

annotated = img.copy()

for cnt in contours:
    area = cv2.contourArea(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)

    if hull_area == 0:
        continue

    solidity = area / hull_area

    x, y, w, h = cv2.boundingRect(cnt)

    if solidity < 0.9:
        cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 0, 255), 2)
    else:
        cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)

comparison = np.hstack((img, annotated))

cv2.imshow("Before vs After Medical", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Analisis Engineering

Solidity didefinisikan sebagai:

Solidity = A / A_convex

Jika objek memiliki cekungan, maka luas convex hull lebih besar dibanding luas asli, sehingga solidity menurun.

Keunggulan:

- Stabil terhadap rotasi.
- Mudah dihitung.
- Cocok untuk deteksi deformasi global.

Kelemahan:

- Sensitif terhadap noise kecil pada batas.
- Hole internal dapat memengaruhi luas secara signifikan.
- Bergantung kuat pada kualitas threshold.

Kompleksitas convex hull adalah O(N log N), sehingga sedikit lebih mahal dibanding circularity dan Hu moments, tetapi masih realistis untuk citra resolusi menengah.

---

# Analisis Engineering Mendalam

1. Kompleksitas Sistem  
   - Ekstraksi kontur: O(N)  
   - Hu Moments: O(N)  
   - Convex Hull: O(N log N)  

2. Sensitivitas Parameter  
   - Threshold memengaruhi topologi objek.  
   - Blur berlebihan mengurangi noise tetapi juga menghilangkan detail bentuk.  

3. Trade-off Desain  
   - Descriptor sederhana → cepat, kurang diskriminatif.  
   - Descriptor invarian → stabil terhadap transformasi, lebih mahal komputasi.  
   - Kombinasi multi-descriptor → robust, tetapi meningkatkan dimensi fitur.  

4. Dampak pada Tahap Lanjutan  
   - Tracking bergantung pada centroid stabil.  
   - OCR bergantung pada stabilitas Hu moments.  
   - Sistem inspeksi industri bergantung pada circularity dan solidity.  

---

# Ringkasan Engineering

Shape descriptor adalah proses transformasi geometri objek ke ruang fitur berdimensi rendah. Keandalan sistem tidak hanya ditentukan oleh rumus matematis descriptor, tetapi terutama oleh kualitas segmentasi awal. Descriptor yang baik harus:

- Stabil terhadap transformasi geometris.
- Robust terhadap noise.
- Efisien secara komputasi.
- Memiliki daya diskriminatif tinggi.

Kesalahan pada tahap segmentasi akan teramplifikasi pada tahap ekstraksi fitur dan berpotensi menyebabkan kegagalan sistem keputusan.

---

# Mini Project Lanjutan

1. Klasifikasi mur dan baut otomatis berbasis circularity dan aspect ratio.  
2. Sistem inspeksi PCB untuk mendeteksi cacat solder berbasis solidity.  
3. Analisis deformasi struktur pada eksperimen shaking table berbasis perubahan Hu moments.  
4. Tracking kendaraan berbasis perubahan bounding box dan centroid.  
5. Sistem sortir buah otomatis berdasarkan circularity dan luas.  
6. Evaluasi perubahan bentuk material elastis akibat stress mekanik.  
7. Shape matching antar citra menggunakan jarak Euclidean pada ruang Hu moments.  
8. Deteksi sel kanker berbasis kombinasi solidity dan eccentricity.  
9. Pengukuran diameter part industri secara otomatis.  
10. Analisis stabilitas bentuk objek terhadap noise buatan untuk evaluasi robustnes descriptor.  

---
```