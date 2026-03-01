# 3.9 Discrete Wavelet Transform (DWT) pada Citra Digital

---

# 1. Pendahuluan

Discrete Wavelet Transform (DWT) merupakan metode transformasi domain frekuensi–spasial berbasis analisis multi-resolusi (Multi-Resolution Analysis / MRA). Berbeda dengan Fourier Transform yang menggunakan basis sinusoidal global, wavelet menggunakan fungsi basis yang terlokalisasi dalam domain spasial dan frekuensi secara simultan.

Secara engineering, DWT memungkinkan:

- Representasi multi-skala
- Pemisahan komponen struktur global dan detail lokal
- Denoising berbasis threshold adaptif
- Kompresi berbasis sparsity koefisien

Dalam pipeline computer vision, DWT umumnya berada pada tahap:

Pre-processing → Feature Extraction → Classification / Detection

---

# 2. Definisi Matematis Formal

## 2.1 Continuous Wavelet Transform

Misalkan sinyal kontinu berada pada ruang Hilbert:

$$
f(t) \in L^2(\mathbb{R})
$$

Continuous Wavelet Transform didefinisikan sebagai:

$$
W(a,b) =
\int_{-\infty}^{\infty}
f(t)\,
\frac{1}{\sqrt{|a|}}\,
\psi\left(\frac{t-b}{a}\right)
dt
$$

dengan:

$$
a \in \mathbb{R}^+ \quad \text{(skala)}
$$

$$
b \in \mathbb{R} \quad \text{(translasi)}
$$

$$
\psi(t) \quad \text{mother wavelet}
$$

Makna simbol:

- a mengontrol resolusi frekuensi
- b mengontrol lokasi spasial
- faktor 1 / sqrt(|a|) menjaga normalisasi energi

Interpretasi matematis: proyeksi sinyal ke basis wavelet ter-skala dan ter-translasi.  
Interpretasi engineering: analisis sinyal lokal pada berbagai resolusi.

---

## 2.2 Diskritisasi (DWT)

Parameter diskrit:

$$
a = 2^j
$$

$$
b = k 2^j
$$

Fungsi wavelet diskrit:

$$
\psi_{j,k}(t) =
2^{-j/2}
\psi(2^{-j}t - k)
$$

Koefisien wavelet:

$$
W_{j,k} =
\langle f(t), \psi_{j,k}(t) \rangle
$$

---

# 3. Multi-Resolution Analysis (MRA)

Ruang fungsi didekomposisi menjadi subruang bertingkat:

$$
\cdots \subset V_{-1} \subset V_0 \subset V_1 \subset \cdots
$$

Relasi penting:

$$
V_{j+1} = V_j \oplus W_j
$$

Makna:

- V_j = ruang aproksimasi
- W_j = ruang detail
- ⊕ = direct sum

Interpretasi engineering:

Citra dapat dipisahkan menjadi:

- Komponen low-frequency (struktur global)
- Komponen high-frequency (tepi dan tekstur)

---

# 4. DWT pada Citra 2D

Filtering separabel menghasilkan 4 subband:

$$
LL = L_x(L_y(I))
$$

$$
LH = L_x(H_y(I))
$$

$$
HL = H_x(L_y(I))
$$

$$
HH = H_x(H_y(I))
$$

I = citra input  
L = low-pass filter  
H = high-pass filter  

---

# 5. Kompleksitas Komputasi

Untuk citra ukuran N × N:

$$
\text{Kompleksitas DWT} = O(N^2)
$$

Dibandingkan FFT:

$$
\text{Kompleksitas FFT} = O(N^2 \log N)
$$

DWT lebih efisien untuk analisis lokal.

---

# 6. Implementasi Dasar DWT

```python
import cv2
import numpy as np
import pywt

img = cv2.imread("input.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

coeffs = pywt.dwt2(gray, 'haar')
LL, (LH, HL, HH) = coeffs

LL = np.uint8(np.clip(LL,0,255))
LH = np.uint8(np.clip(LH,0,255))
HL = np.uint8(np.clip(HL,0,255))
HH = np.uint8(np.clip(HH,0,255))

top = np.hstack((LL, LH))
bottom = np.hstack((HL, HH))
comparison = np.vstack((top, bottom))

cv2.imshow("DWT Subbands", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# 7. Studi Kasus Teknik Lapangan

---

## 7.1 Denoising Citra Medis

Model noise Gaussian:

$$
I_{noisy}(x,y) = I(x,y) + n(x,y)
$$

$$
n(x,y) \sim \mathcal{N}(0,\sigma^2)
$$

Soft threshold:

$$
\hat{w} =
\begin{cases}
\text{sign}(w)(|w|-T), & |w| > T \\
0, & lainnya
\end{cases}
$$

```python
import cv2
import numpy as np
import pywt

img = cv2.imread("xray.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

coeffs = pywt.dwt2(gray, 'haar')
LL, (LH, HL, HH) = coeffs

T = 20

LH = pywt.threshold(LH, T, mode='soft')
HL = pywt.threshold(HL, T, mode='soft')
HH = pywt.threshold(HH, T, mode='soft')

denoised = pywt.idwt2((LL,(LH,HL,HH)), 'haar')
denoised = np.uint8(np.clip(denoised,0,255))

comparison = np.hstack((gray, denoised))

cv2.imshow("Wavelet Denoising", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Analisis:

- Threshold kecil → noise tersisa
- Threshold besar → detail hilang

---

## 7.2 Kompresi Citra Industri

Hard threshold:

$$
w =
\begin{cases}
w, & |w| > T \\
0, & lainnya
\end{cases}
$$

```python
import cv2
import numpy as np
import pywt

img = cv2.imread("metal.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

coeffs = pywt.wavedec2(gray, 'haar', level=2)

threshold = 30

coeffs_thresh = []
for c in coeffs:
    if isinstance(c, tuple):
        coeffs_thresh.append(tuple(pywt.threshold(x, threshold, mode='hard') for x in c))
    else:
        coeffs_thresh.append(c)

reconstructed = pywt.waverec2(coeffs_thresh, 'haar')
reconstructed = np.uint8(np.clip(reconstructed,0,255))

comparison = np.hstack((gray, reconstructed))

cv2.imshow("Wavelet Compression", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Trade-off:

- Rasio kompresi naik
- Risiko kehilangan detail mikro

---

## 7.3 Ekstraksi Fitur Tekstur

Energi subband:

$$
E = \sum_{i,j} |W_{i,j}|^2
$$

```python
import cv2
import numpy as np
import pywt

img = cv2.imread("fabric.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

coeffs = pywt.wavedec2(gray, 'db2', level=2)

features = []

for coeff in coeffs[1:]:
    for c in coeff:
        energy = np.sum(np.square(c))
        features.append(energy)

print("Feature Energy:", features)

LL = coeffs[0]
LL = np.uint8(np.clip(LL,0,255))

comparison = np.hstack((gray[:LL.shape[0], :LL.shape[1]], LL))

cv2.imshow("Texture LL", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# 8. Analisis Engineering Mendalam

Parameter kritis:

- Jenis wavelet
- Level dekomposisi
- Threshold

Risiko desain:

- Over-smoothing
- Artefak rekonstruksi
- Distorsi fitur untuk tahap klasifikasi

Dampak pada pipeline:

- Mengubah performa contour detection
- Mempengaruhi OCR
- Mempengaruhi feature matching

---

# 9. Ringkasan Engineering

DWT memberikan representasi multi-skala yang efisien secara komputasi dan kuat untuk analisis lokal. Cocok untuk:

- Denoising
- Kompresi
- Ekstraksi fitur

Kurang optimal untuk analisis periodik global.

Wavelet merupakan fondasi penting dalam transform-domain vision system modern.

---

# 10. Mini Project Lanjutan

- Analisis threshold optimal berbasis estimasi variansi noise
- Perbandingan Haar vs Daubechies
- Integrasi DWT + SVM
- DWT untuk deteksi retakan beton
- Video denoising real-time
- Watermarking berbasis DWT
- Hybrid FFT + DWT
- Evaluasi sparsity koefisien
- Pre-processing OCR dokumen rusak
- Analisis performa CPU vs GPU