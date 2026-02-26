# 3.2 Transformasi Geometris pada Citra

Transformasi geometris adalah operasi yang memodifikasi posisi spasial piksel pada citra tanpa secara langsung mengubah nilai intensitasnya. Dalam pemrosesan citra digital, sebuah citra dapat dipandang sebagai fungsi dua variabel:

$$
f(x, y)
$$

di mana setiap pasangan koordinat $(x, y)$ merepresentasikan posisi piksel dan $f$ menyatakan nilai intensitas (untuk citra grayscale) atau vektor warna (untuk citra RGB/BGR) pada titik tersebut.

Transformasi geometris bekerja dengan memetakan koordinat awal $(x, y)$ menjadi koordinat baru $(x', y')$. Dengan kata lain, transformasi ini tidak mengubah nilai piksel secara langsung, tetapi mengubah **di mana piksel tersebut ditempatkan** pada domain spasial.

---

## Representasi Matriks Homogen

Untuk memahami transformasi geometris secara umum, kita tidak cukup menggunakan matriks 2×2 biasa.  
Hal ini karena translasi tidak dapat direpresentasikan sebagai perkalian matriks linear murni.

Oleh karena itu digunakan **koordinat homogen**, yaitu dengan menambahkan satu dimensi tambahan sehingga koordinat 2D:

$$
(x, y)
$$

dituliskan menjadi:

$$
(x, y, 1)
$$

Dengan pendekatan ini, transformasi umum dapat dituliskan sebagai:

$$
\begin{bmatrix}
x' \\
y' \\
1
\end{bmatrix}
=
\begin{bmatrix}
a & b & c \\
d & e & f \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
x \\
y \\
1
\end{bmatrix}
$$

Matriks 3×3 ini disebut **matriks transformasi homogen 2D**.

---

### Interpretasi Elemen Matriks

Jika kita uraikan:

$$
x' = ax + by + c
$$

$$
y' = dx + ey + f
$$

- Elemen `a, b, d, e` → mengatur rotasi, scaling, dan shear.
- Elemen `c, f` → merepresentasikan translasi.
- Baris terakhir `[0 0 1]` → menjaga konsistensi koordinat homogen.

---

### Mengapa Pendekatan Ini Penting?

Dengan matriks homogen:

1. Translasi dapat direpresentasikan dalam bentuk matriks.
2. Rotasi dapat dikombinasikan dengan translasi.
3. Scaling dan shear dapat digabungkan.
4. Beberapa transformasi dapat dikalikan menjadi satu matriks tunggal:

$$
M_{total} = M_3 \cdot M_2 \cdot M_1
$$

Artinya, sistem transformasi menjadi:

- Modular
- Komposisional
- Stabil secara matematis

Pendekatan ini adalah fondasi dalam:

- Robotika (transformasi frame koordinat)
- Augmented Reality (pose estimation)
- Kalibrasi kamera
- Sistem navigasi visual
- Computer graphics

---

## Konsep Warping

Dalam implementasi OpenCV, transformasi geometris dilakukan melalui proses yang disebut **warping**.

Warping bukan hanya memindahkan piksel, tetapi melakukan dua langkah penting:

### 1. Transformasi Koordinat

Untuk setiap piksel pada citra output, sistem menghitung koordinat asalnya pada citra input menggunakan matriks transformasi.

OpenCV menggunakan pendekatan **inverse mapping**:

Daripada memetakan piksel sumber ke tujuan (yang bisa menyebabkan lubang kosong), OpenCV menghitung:

> Untuk setiap piksel output, dari mana asal piksel tersebut pada citra input?

Pendekatan ini lebih stabil dan menghindari pixel holes.

---

### 2. Interpolasi

Masalah muncul karena hasil transformasi sering menghasilkan koordinat pecahan (floating point).

Contoh:

$$
(x', y') = (102.4, 56.7)
$$

Karena piksel hanya berada pada koordinat diskrit, diperlukan metode interpolasi untuk menentukan nilai intensitasnya.

OpenCV menyediakan beberapa metode:

- `INTER_NEAREST`  
  Mengambil piksel terdekat. Cepat tetapi kasar.

- `INTER_LINEAR`  
  Interpolasi linear dua arah. Seimbang antara kualitas dan performa.

- `INTER_CUBIC`  
  Interpolasi kubik. Lebih halus tetapi komputasi lebih berat.

- `INTER_AREA`  
  Cocok untuk downsampling karena mempertimbangkan area piksel.

---

### Dampak Interpolasi terhadap Sistem

Pilihan interpolasi memengaruhi:

- Ketajaman citra
- Artefak aliasing
- Akurasi fitur
- Stabilitas sistem tracking

Dalam sistem teknik:

- Downsampling dataset → gunakan `INTER_AREA`
- Upsampling citra medis → gunakan `INTER_CUBIC`
- Sistem real-time → gunakan `INTER_LINEAR`
- Sistem sangat cepat → gunakan `INTER_NEAREST`

---

## Insight Engineering

Transformasi geometris bukan hanya manipulasi gambar, tetapi manipulasi domain spasial.

Dengan memahami matriks homogen dan warping:

- Kita memahami bagaimana sistem vision menyesuaikan perspektif.
- Kita dapat menggabungkan transformasi secara matematis.
- Kita dapat menganalisis kesalahan geometris secara sistematis.
- Kita siap masuk ke topik lanjutan seperti homografi dan epipolar geometry.
---

## Forward vs Inverse Mapping

### Forward Mapping
Memetakan piksel sumber ke tujuan → dapat menghasilkan lubang kosong.

### Inverse Mapping (Digunakan OpenCV)
Untuk setiap piksel tujuan, sistem mencari asalnya di citra sumber → lebih stabil.

---

# 3.2.1 Translasi

## Teori

$$
x' = x + t_x
$$
$$
y' = y + t_y
$$

Matriks translasi:

$$
\begin{bmatrix}
1 & 0 & t_x \\
0 & 1 & t_y
\end{bmatrix}
$$

---

## Contoh — Translasi

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")
rows, cols = img.shape[:2]

M = np.float32([[1, 0, 50],
                [0, 1, 30]])

dst = cv2.warpAffine(img, M, (cols, rows))

comparison = np.hstack((img, dst))
cv2.imshow("Left: Original | Right: Translation", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight
- 50 → geser kanan 50 piksel
- 30 → geser bawah 30 piksel
- Area kosong berwarna hitam

---

# 3.2.2 Rotasi

## Teori

$$
\begin{bmatrix}
x' \\
y'
\end{bmatrix}
=
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
\begin{bmatrix}
x \\
y
\end{bmatrix}
$$

---

## Contoh — Rotasi

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")
rows, cols = img.shape[:2]

M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
dst = cv2.warpAffine(img, M, (cols, rows))

comparison = np.hstack((img, dst))
cv2.imshow("Left: Original | Right: Rotation 45 deg", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight
- Rotasi dapat menyebabkan cropping
- Termasuk affine transform

---

# 3.2.3 Scaling

## Teori

$$
x' = s_x x
$$
$$
y' = s_y y
$$

---

## Contoh — Scaling

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

scaled = cv2.resize(img, None, fx=0.5, fy=0.5,
                    interpolation=cv2.INTER_LINEAR)

scaled_back = cv2.resize(scaled, (img.shape[1], img.shape[0]))

comparison = np.hstack((img, scaled_back))
cv2.imshow("Left: Original | Right: Scaled Down-Up", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight
- INTER_AREA baik untuk downsampling
- INTER_CUBIC baik untuk upsampling

---

# 3.2.4 Affine Transform

## Teori

Affine mempertahankan garis sejajar. Membutuhkan 3 titik referensi.

---

## Contoh — Affine

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")
rows, cols = img.shape[:2]

pts1 = np.float32([[50,50],
                   [200,50],
                   [50,200]])

pts2 = np.float32([[10,100],
                   [200,50],
                   [100,250]])

M = cv2.getAffineTransform(pts1, pts2)
dst = cv2.warpAffine(img, M, (cols, rows))

comparison = np.hstack((img, dst))
cv2.imshow("Left: Original | Right: Affine", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight
- Garis sejajar tetap sejajar
- Tidak mengoreksi perspektif

---

# 3.2.5 Perspective Transform

## Teori

Perspective transform menggunakan matriks homografi 3x3 dan membutuhkan 4 titik referensi.

---

## Contoh — Perspective

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

pts1 = np.float32([[56,65],
                   [368,52],
                   [28,387],
                   [389,390]])

pts2 = np.float32([[0,0],
                   [300,0],
                   [0,300],
                   [300,300]])

M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (300,300))

comparison = np.hstack((img, cv2.resize(dst, (img.shape[1], img.shape[0]))))
cv2.imshow("Left: Original | Right: Perspective", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Insight
- Garis sejajar dapat berubah
- Digunakan pada document scanner dan bird-eye view

---

# Ringkasan Bab 3.2

1. Transformasi geometris memodifikasi koordinat piksel.
2. Translasi menggeser posisi citra.
3. Rotasi mengubah orientasi.
4. Scaling mengubah ukuran.
5. Affine mempertahankan garis sejajar.
6. Perspective mengubah struktur perspektif.
7. WarpAffine menggunakan matriks 2x3.
8. WarpPerspective menggunakan matriks 3x3.
9. Interpolasi memengaruhi kualitas hasil.
10. Inverse mapping menghindari lubang piksel.
11. Transformasi penting dalam normalisasi dataset.
12. Digunakan dalam koreksi kamera.
13. Digunakan dalam kendaraan otonom.
14. Digunakan dalam augmented reality.
15. Fondasi sistem visi spasial modern.

---

# Ide Mini Project

1. Mini document scanner otomatis.
2. Bird-eye view kamera parkir.
3. Dataset augmentation tool.
4. Simulator rotasi objek industri.
5. Koreksi kemiringan papan tulis.
6. Kalibrasi kamera sederhana.
7. Visual tool transformasi interaktif.
8. Normalisasi orientasi objek sebelum klasifikasi.
9. Dashboard eksperimen interpolasi.
10. Preprocessing OCR berbasis perspective transform.