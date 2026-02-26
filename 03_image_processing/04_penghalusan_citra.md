# 3.4 Penghalusan Citra (Image Smoothing / Filtering)

Penghalusan citra adalah proses reduksi variasi intensitas lokal untuk mengurangi noise dan detail frekuensi tinggi.  

Secara matematis, citra grayscale dapat direpresentasikan sebagai fungsi diskrit dua dimensi:

$$
f(x,y)
$$

Noise pada citra dapat dipandang sebagai komponen acak yang ditambahkan pada sinyal asli:

$$
g(x,y) = f(x,y) + n(x,y)
$$

dengan:
- $f(x,y)$ → citra asli
- $n(x,y)$ → noise
- $g(x,y)$ → citra teramati

Tujuan smoothing adalah memperkirakan kembali $f(x,y)$ dari $g(x,y)$ dengan menekan komponen $n(x,y)$.

---

# 3.4.1 Konsep Dasar Filtering Spasial

Filtering spasial dilakukan menggunakan **kernel (mask) konvolusi**.

Secara umum, operasi konvolusi dua dimensi didefinisikan sebagai:

$$
g(x,y) = \sum_{i=-k}^{k} \sum_{j=-k}^{k} h(i,j)\, f(x-i, y-j)
$$

di mana:

- $h(i,j)$ → kernel filter
- $f(x,y)$ → citra input
- $g(x,y)$ → citra hasil

Konvolusi adalah operasi linear dan bersifat shift-invariant.

---

## Interpretasi Frekuensi

Dalam domain frekuensi:

- Detail tajam → frekuensi tinggi
- Perubahan lambat → frekuensi rendah

Smoothing adalah **low-pass filtering**, yaitu melewatkan frekuensi rendah dan menekan frekuensi tinggi.

---

# 3.4.2 Average Blur (Mean Filter)

## Teori

Mean filter mengganti setiap piksel dengan rata-rata nilai piksel dalam neighborhood berukuran $k \times k$:

$$
g(x,y) = \frac{1}{k^2} \sum_{i=-r}^{r} \sum_{j=-r}^{r} f(x+i, y+j)
$$

Filter ini efektif untuk noise Gaussian ringan, tetapi mengaburkan tepi.

---

## Struktur Fungsi

```
cv2.blur(src, ksize)
```

---

## Contoh — Mean Filter

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

blur = cv2.blur(img, (5,5))

comparison = np.hstack((img, blur))

cv2.imshow("Original | Mean Blur 5x5", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### Insight Engineering

- Kernel besar → smoothing lebih kuat
- Tepi objek ikut terblur
- Cepat dan sederhana
- Cocok untuk preprocessing ringan

---

# 3.4.3 Gaussian Blur

## Teori

Gaussian filter menggunakan distribusi Gaussian 2D:

$$
G(x,y) = \frac{1}{2\pi\sigma^2}
\exp\left(-\frac{x^2 + y^2}{2\sigma^2}\right)
$$

Properti penting:

- Isotropik
- Smooth secara diferensial
- Tidak menghasilkan artefak tajam

Gaussian blur ekuivalen dengan konvolusi citra dengan kernel Gaussian.

---

## Struktur Fungsi

```
cv2.GaussianBlur(src, ksize, sigmaX)
```

---

## Contoh — Gaussian Blur

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

gauss_small = cv2.GaussianBlur(img, (5,5), 0)
gauss_large = cv2.GaussianBlur(img, (15,15), 0)

comparison = np.hstack((img, gauss_small, gauss_large))

cv2.imshow("Original | Gaussian 5x5 | Gaussian 15x15", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### Insight Engineering

- Kernel besar → detail kecil hilang
- Lebih natural dibanding mean
- Digunakan sebelum Canny edge detection
- Penting dalam Otsu preprocessing

---

# 3.4.4 Median Filter

## Teori

Median filter adalah filter non-linear.

Setiap piksel diganti dengan median neighborhood:

$$
g(x,y) = \text{median} \{ f(x+i, y+j) \}
$$

Keunggulan:
- Sangat efektif untuk **salt-and-pepper noise**
- Mempertahankan tepi lebih baik dari mean

---

## Struktur Fungsi

```
cv2.medianBlur(src, ksize)
```

---

## Contoh — Median Filter

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

median = cv2.medianBlur(img, 5)

comparison = np.hstack((img, median))

cv2.imshow("Original | Median 5x5", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### Insight Engineering

- Non-linear → tidak dapat dianalisis dengan teori frekuensi klasik
- Cocok untuk noise impuls
- Lebih mahal komputasi dibanding mean

---

# 3.4.5 Bilateral Filter

## Teori

Bilateral filter mempertimbangkan dua jarak:

1. Jarak spasial
2. Jarak intensitas

Rumusnya:

$$
g(x) = \frac{1}{W_p}
\sum_{x_i \in \Omega}
f(x_i)\,
\exp\left(-\frac{\|x_i-x\|^2}{2\sigma_s^2}\right)
\exp\left(-\frac{\|f(x_i)-f(x)\|^2}{2\sigma_r^2}\right)
$$

dengan:
- $\sigma_s$ → kontrol jarak spasial
- $\sigma_r$ → kontrol perbedaan intensitas
- $W_p$ → faktor normalisasi

Keunggulan:
- Menghaluskan noise
- Mempertahankan tepi

---

## Struktur Fungsi

```
cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace)
```

---

## Contoh — Bilateral Filter

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

bilateral = cv2.bilateralFilter(img, 9, 75, 75)

comparison = np.hstack((img, bilateral))

cv2.imshow("Original | Bilateral", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### Insight Engineering

- Edge preserved smoothing
- Cocok untuk preprocessing segmentation
- Komputasi mahal
- Banyak digunakan dalam face beautification dan depth map refinement

---

# 3.4.6 Perbandingan Semua Filter

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

mean = cv2.blur(img, (5,5))
gauss = cv2.GaussianBlur(img, (5,5), 0)
median = cv2.medianBlur(img, 5)
bilateral = cv2.bilateralFilter(img, 9, 75, 75)

comparison = np.hstack((img, mean, gauss, median, bilateral))

cv2.imshow("Original | Mean | Gaussian | Median | Bilateral", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# Analisis Engineering

| Filter | Linear | Preserves Edge | Noise Type | Komputasi |
|--------|--------|----------------|------------|-----------|
| Mean | Ya | Tidak | Gaussian ringan | Cepat |
| Gaussian | Ya | Tidak | Gaussian | Cepat |
| Median | Tidak | Cukup | Salt-pepper | Sedang |
| Bilateral | Tidak | Ya | Campuran | Mahal |

---

# Dampak terhadap Pipeline Computer Vision

Smoothing memengaruhi:

- Kualitas thresholding
- Stabilitas edge detection
- Akurasi contour detection
- Robustness feature extraction

Over-smoothing dapat menghilangkan detail penting.

Under-smoothing membuat noise dominan.

Trade-off adalah inti desain sistem vision.

---

# Ringkasan Bab 3.4

1. Smoothing adalah low-pass filtering.
2. Konvolusi adalah dasar filtering linear.
3. Mean sederhana tetapi mengaburkan tepi.
4. Gaussian lebih natural dan stabil.
5. Median efektif untuk salt-and-pepper.
6. Bilateral mempertahankan tepi.
7. Kernel size memengaruhi detail hilang.
8. Sigma menentukan kekuatan smoothing.
9. Filtering memengaruhi histogram.
10. Smoothing adalah tahap preprocessing penting.

---

# Ide Mini Project

1. Bandingkan performa filter terhadap noise sintetis.
2. Uji pengaruh smoothing pada Otsu.
3. Analisis edge sebelum dan sesudah blur.
4. Optimasi bilateral untuk sistem real-time.
5. Studi efek kernel size terhadap detail mikro.
6. Noise simulation dan recovery analysis.
7. Visualisasi spektrum frekuensi sebelum–sesudah.
8. Integrasi smoothing dalam pipeline segmentasi.
9. Analisis PSNR dan SSIM hasil smoothing.
10. Eksperimen trade-off blur vs edge retention.