# 04_advanced_processing/04_image_registration.md

# Bab 04 — Advanced Processing  
# 04 — Image Registration (Registrasi Citra)

---

# 1. Posisi Image Registration dalam Pipeline Computer Vision

Dalam sistem computer vision tingkat lanjut, image registration merupakan tahap fundamental ketika dua atau lebih citra harus dipetakan ke sistem koordinat yang sama sebelum analisis lebih lanjut dilakukan.

Pipeline umum:

Akuisisi → Preprocessing → Feature Extraction → **Registration** → Fusion / Change Detection / Tracking / Measurement

Kesalahan pada tahap registration akan menyebabkan:

- Error geometri pada contour analysis
- Distorsi pengukuran area atau panjang
- Kesalahan pada optical flow
- Kegagalan stitching panorama
- Error pada sistem inspeksi industri

Secara engineering, registration adalah problem optimasi parameter transformasi geometris terhadap fungsi kesesuaian citra.

---

# 2. Formulasi Matematis Umum

Misalkan:

$$
I_s(x,y)
$$

adalah citra sumber (source image)

$$
I_r(x,y)
$$

adalah citra referensi (reference image)

Tujuan registrasi adalah menemukan transformasi parametrik:

$$
T_\theta : \mathbb{R}^2 \rightarrow \mathbb{R}^2
$$

dengan parameter:

$$
\theta = (\theta_1, \theta_2, ..., \theta_n)
$$

sehingga memaksimalkan fungsi similarity:

$$
\theta^* = \arg \max_\theta \mathcal{S}
\left(
I_r(x,y), I_s(T_\theta(x,y))
\right)
$$

di mana:

- $T_\theta(x,y)$ adalah koordinat hasil transformasi
- $\mathcal{S}$ adalah fungsi kesamaan
- $\theta^*$ adalah parameter optimal

Secara engineering, ini adalah problem optimasi non-linear.

---

# 3. Model Transformasi Geometris

## 3.1 Translasi

$$
\begin{bmatrix}
x' \\
y'
\end{bmatrix}
=
\begin{bmatrix}
x \\
y
\end{bmatrix}
+
\begin{bmatrix}
t_x \\
t_y
\end{bmatrix}
$$

Parameter:
- $t_x$ translasi horizontal
- $t_y$ translasi vertikal

Derajat kebebasan: 2

---

## 3.2 Transformasi Affine

$$
\begin{bmatrix}
x' \\
y'
\end{bmatrix}
=
\begin{bmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{bmatrix}
\begin{bmatrix}
x \\
y
\end{bmatrix}
+
\begin{bmatrix}
t_x \\
t_y
\end{bmatrix}
$$

Parameter: 6

Mampu memodelkan:
- Rotasi
- Skala
- Shear
- Translasi

---

## 3.3 Homografi (Projective Transformation)

Dalam koordinat homogen:

$$
\begin{bmatrix}
x' \\
y' \\
w'
\end{bmatrix}
=
H
\begin{bmatrix}
x \\
y \\
1
\end{bmatrix}
$$

dengan:

$$
H =
\begin{bmatrix}
h_{11} & h_{12} & h_{13} \\
h_{21} & h_{22} & h_{23} \\
h_{31} & h_{32} & h_{33}
\end{bmatrix}
$$

Koordinat akhir:

$$
x' = \frac{h_{11}x + h_{12}y + h_{13}}
{h_{31}x + h_{32}y + h_{33}}
$$

$$
y' = \frac{h_{21}x + h_{22}y + h_{23}}
{h_{31}x + h_{32}y + h_{33}}
$$

Derajat kebebasan: 8

Digunakan untuk scene planar dengan perubahan perspektif.

---

# 4. Fungsi Similarity

## 4.1 Sum of Squared Differences (SSD)

$$
SSD = \sum_{x,y}
\left(
I_r(x,y) - I_s(T_\theta(x,y))
\right)^2
$$

Sensitif terhadap perubahan intensitas global.

---

## 4.2 Normalized Cross Correlation (NCC)

$$
NCC =
\frac{
\sum (I_r - \mu_r)(I_s - \mu_s)
}
{
\sqrt{
\sum (I_r - \mu_r)^2
\sum (I_s - \mu_s)^2
}
}
$$

Lebih robust terhadap pencahayaan.

---

## 4.3 Enhanced Correlation Coefficient (ECC)

Digunakan pada OpenCV untuk optimasi iteratif berbasis gradien.

---

# 5. Kompleksitas Komputasi

Feature-based registration:

- Deteksi fitur: $O(N)$
- Matching: $O(N \log N)$
- RANSAC: $O(kN)$

ECC iterative alignment:

- Kompleksitas: $O(iteration \times pixel)$
- Sensitif terhadap inisialisasi

Trade-off utama:

Feature-based → robust transformasi besar  
ECC → presisi tinggi transformasi kecil  

---

# STUDI KASUS 1  
## Registrasi Dokumen untuk OCR

### Permasalahan Lapangan

Dokumen difoto dari sudut miring. OCR membutuhkan citra yang sejajar.

### Pipeline

Grayscale → ORB → Matching → Homography → Warp

---

## Kode Lengkap

```python
import cv2
import numpy as np

img_ref = cv2.imread('doc_ref.jpg')
img_src = cv2.imread('doc_miring.jpg')

gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
gray_src = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create(1500)

kp1, des1 = orb.detectAndCompute(gray_ref, None)
kp2, des2 = orb.detectAndCompute(gray_src, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)

pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)

H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, 5.0)

height, width = img_ref.shape[:2]
aligned = cv2.warpPerspective(img_src, H, (width, height))

comparison = np.hstack((img_ref, aligned))

cv2.imshow("Document Registration", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()

```

## Analisis Engineering — Studi Kasus 1 (Homografi + RANSAC)

Parameter `ransacReprojThreshold` pada algoritma RANSAC menentukan batas maksimum reprojection error yang masih diklasifikasikan sebagai inlier. Reprojection error didefinisikan sebagai jarak Euclidean antara titik observasi aktual dan titik hasil proyeksi menggunakan matriks homografi $H$.

Jika threshold terlalu besar, maka titik korespondensi yang sebenarnya merupakan outlier tetap diterima sebagai inlier. Dampaknya:

- Estimasi matriks homografi $H$ menjadi bias  
- Distorsi perspektif muncul pada citra hasil `warpPerspective`  
- Kesalahan geometri terakumulasi pada tahap lanjutan  

Sebaliknya, jika threshold terlalu kecil, maka banyak pasangan titik valid ditolak. Konsekuensinya:

- Jumlah inlier tidak mencukupi (minimal 4 titik non-kolinear)  
- Homografi gagal dihitung  
- Solusi menjadi tidak stabil secara numerik  

Secara teoritis, model homografi hanya valid untuk:

- Scene planar, atau  
- Kamera mengalami rotasi murni tanpa translasi relatif terhadap objek yang sangat jauh  

Untuk objek non-planar dengan variasi kedalaman signifikan, model homografi akan menghasilkan misalignment lokal karena asumsi satu bidang proyeksi tidak terpenuhi.

---

# STUDI KASUS 2  
## Registrasi Medis Menggunakan Affine + ECC  

### Permasalahan Lapangan

Pada pencitraan X-ray thorax, dua citra dapat mengalami pergeseran kecil akibat pernapasan pasien. Pergeseran ini biasanya berupa translasi kecil dan deformasi linear ringan. Registrasi diperlukan untuk:

- Monitoring progres penyakit  
- Analisis perubahan jaringan  
- Evaluasi pertumbuhan abnormalitas  

Model yang digunakan adalah transformasi affine dengan optimasi Enhanced Correlation Coefficient (ECC).

---

## Kode Lengkap

```python
import cv2
import numpy as np

# Membaca citra
img1 = cv2.imread('xray1.jpg')
img2 = cv2.imread('xray2.jpg')

# Konversi ke grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Mode transformasi affine
warp_mode = cv2.MOTION_AFFINE

# Inisialisasi matriks affine 2x3
warp_matrix = np.eye(2, 3, dtype=np.float32)

# Kriteria terminasi optimasi
criteria = (
    cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
    5000,
    1e-6
)

# Estimasi transformasi menggunakan ECC
(cc, warp_matrix) = cv2.findTransformECC(
    gray1,
    gray2,
    warp_matrix,
    warp_mode,
    criteria
)

# Warp citra kedua
aligned = cv2.warpAffine(
    img2,
    warp_matrix,
    (img1.shape[1], img1.shape[0])
)

# Visualisasi perbandingan
comparison = np.hstack((img1, aligned))

cv2.imshow("Medical Registration ECC", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Analisis Engineering

ECC memaksimalkan koefisien korelasi ter-normalisasi:

$$
\rho =
\frac{\sum I_r(x,y)\, I_s(x,y)}
{\sqrt{\sum I_r(x,y)^2 \; \sum I_s(x,y)^2}}
$$

Optimasi dilakukan secara iteratif dengan pendekatan berbasis gradien terhadap parameter transformasi.

Karakteristik metode:

- Sensitif terhadap inisialisasi awal  
- Efektif untuk transformasi kecil  
- Tidak robust terhadap perubahan perspektif besar  

Jika perbedaan awal antar citra terlalu besar, optimasi dapat terjebak pada local optimum dan gagal konvergen.

Kompleksitas komputasi dapat diperkirakan:

$$
O(N \times k)
$$

dengan:
- $N$ = jumlah piksel  
- $k$ = jumlah iterasi  

Semakin tinggi resolusi citra, semakin besar beban komputasi.

---

# STUDI KASUS 3  
## Registrasi Citra Drone untuk Pemetaan  

### Permasalahan Lapangan

Dua citra drone dengan area overlap digunakan untuk membangun peta lahan. Terdapat:

- Perubahan perspektif  
- Translasi relatif besar  
- Potensi mismatch fitur akibat variasi tekstur  

Registrasi dilakukan menggunakan pendekatan feature-based (ORB + RANSAC + Homography).

---

## Kode Lengkap

```python
import cv2
import numpy as np

# Membaca citra
img1 = cv2.imread('drone1.jpg')
img2 = cv2.imread('drone2.jpg')

# Konversi ke grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Detektor ORB
orb = cv2.ORB_create(2000)

kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)

# Brute-force matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Ekstraksi titik korespondensi
pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)

# Estimasi homografi
H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, 4.0)

# Warp perspektif
result = cv2.warpPerspective(
    img2,
    H,
    (img1.shape[1] + img2.shape[1], img1.shape[0])
)

# Overlay citra pertama
result[0:img1.shape[0], 0:img1.shape[1]] = img1

# Visualisasi perbandingan
comparison = np.hstack((img1, result[:, :img1.shape[1]]))

cv2.imshow("Drone Registration", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Analisis Engineering

Jumlah fitur memengaruhi stabilitas homografi:

- Terlalu sedikit fitur → sistem underdetermined → solusi tidak stabil  
- Terlalu banyak fitur → waktu komputasi meningkat  

RANSAC mengeliminasi outlier akibat mismatch, namun nilai threshold menentukan toleransi reprojection error.

Registrasi yang buruk dalam pemetaan menyebabkan:

- Kesalahan estimasi luas area  
- Distorsi batas lahan  
- Error pada pengukuran jarak  

---

# Dampak Terhadap Tahap Lanjutan

Kesalahan registration menghasilkan efek sistemik:

- Distorsi kontur → error pada contour analysis  
- Bounding box meleset → object detection tidak akurat  
- OCR gagal akibat misalignment  
- Drift pada tracking multi-frame  
- Artefak visual pada panorama  

Registration merupakan fondasi geometris dalam pipeline computer vision.

---

# Ringkasan Engineering

Image registration adalah problem optimasi parameter transformasi geometris untuk menyelaraskan domain koordinat dua citra. Model transformasi harus dipilih berdasarkan kondisi fisik sistem dan asumsi geometri scene.

Feature-based registration lebih fleksibel untuk transformasi besar dan perubahan perspektif. ECC lebih presisi untuk pergeseran kecil dan deformasi ringan.

Kesalahan pemilihan parameter atau model transformasi berdampak sistemik pada seluruh pipeline computer vision.

---

# Mini Project Lanjutan

1. Evaluasi Reprojection Error pada Homografi  
   Hitung reprojection error rata-rata dan variansinya setelah estimasi homografi. Analisis hubungan antara jumlah inlier, threshold RANSAC, dan stabilitas matriks $H$. Lakukan eksperimen dengan berbagai nilai threshold dan plot kurva error terhadap jumlah inlier.

2. Perbandingan ORB dan SIFT terhadap Noise Gaussian  
   Tambahkan noise Gaussian dengan variansi berbeda pada citra, kemudian bandingkan jumlah keypoint terdeteksi, jumlah inlier, serta error registrasi. Analisis robustness masing-masing deskriptor terhadap degradasi sinyal.

3. Implementasi Multiscale Registration  
   Terapkan registrasi bertingkat menggunakan image pyramid (Gaussian pyramid). Lakukan estimasi transformasi pada resolusi rendah terlebih dahulu, lalu refine pada resolusi lebih tinggi. Evaluasi peningkatan konvergensi dan stabilitas.

4. Registrasi RGB dan Infrared Menggunakan Mutual Information  
   Implementasikan fungsi mutual information sebagai similarity metric untuk citra multi-modal. Bandingkan hasilnya dengan NCC dan ECC pada kasus perbedaan distribusi intensitas.

5. Evaluasi Konvergensi ECC terhadap Variasi Inisialisasi  
   Uji beberapa inisialisasi matriks transformasi awal dan ukur jumlah iterasi hingga konvergen. Analisis kecenderungan terjebak pada local optimum.

6. Analisis Pengaruh Jumlah Fitur terhadap Stabilitas Transformasi  
   Variasikan parameter jumlah fitur pada ORB/SIFT (misalnya 500, 1000, 2000, 5000). Ukur reprojection error dan waktu komputasi. Evaluasi trade-off antara akurasi dan kompleksitas.

7. Implementasi Video Stabilization Berbasis Registration  
   Gunakan registrasi frame-to-frame untuk menghitung transformasi global, lalu lakukan smoothing parameter transformasi menggunakan moving average atau Kalman filter. Evaluasi pengurangan jitter.

8. Panorama Blending Multiband  
   Setelah registrasi berhasil, implementasikan multiband blending menggunakan Laplacian pyramid untuk mengurangi seam artefacts. Bandingkan dengan blending linear sederhana.

9. Registration Berbasis Optical Flow  
   Gunakan dense optical flow untuk menghitung field pergeseran piksel, lalu estimasi transformasi global dari flow field tersebut. Bandingkan dengan pendekatan feature-based.

10. Evaluasi Robustness terhadap Blur dan Noise  
    Tambahkan Gaussian blur dan motion blur dengan kernel berbeda. Uji stabilitas registrasi dan ukur degradasi akurasi terhadap tingkat blur.

    ---