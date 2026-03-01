# 4.3 — Hough Transform

---

# 1. Pendahuluan dan Posisi dalam Pipeline

Pipeline umum sistem computer vision:

Akuisisi → Preprocessing → Edge Detection → Representasi Geometri → Analisis → Keputusan

Hough Transform berada pada tahap **representasi geometri parametrik**, yaitu mendeteksi struktur matematis global (garis, lingkaran) dari sekumpulan piksel tepi.

Berbeda dengan contour analysis yang bekerja pada objek tersegmentasi, Hough Transform bekerja langsung pada edge map sehingga:

- Robust terhadap fragmentasi kontur  
- Tahan noise moderat  
- Tidak membutuhkan kontur tertutup  

Secara matematis, metode ini memetakan pencarian bentuk di domain spasial menjadi pencarian maksimum pada domain parameter.

---

# 2. Formulasi Matematis Hough Transform untuk Garis

## 2.1 Representasi Garis

Representasi kartesian:

$$
y = mx + c
$$

Tidak stabil untuk garis vertikal karena:

$$
m \to \infty
$$

Digunakan bentuk normal:

$$
\rho = x\cos\theta + y\sin\theta
$$

Dengan:

- $(x,y)$ = koordinat piksel  
- $\theta$ = sudut normal garis  
- $\rho$ = jarak terhadap origin  

---

## 2.2 Transformasi ke Ruang Parameter

Untuk setiap piksel tepi $(x_i,y_i)$:

$$
\rho(\theta) = x_i\cos\theta + y_i\sin\theta
$$

Setiap piksel menghasilkan kurva sinusoidal pada ruang $(\rho,\theta)$.

Accumulator:

$$
A(\rho,\theta)
$$

Voting:

$$
A(\rho,\theta) = A(\rho,\theta) + 1
$$

Deteksi jika:

$$
A(\rho,\theta) \ge \tau
$$

---

## 2.3 Kompleksitas

Jika:

- $N$ = jumlah piksel tepi  
- $T$ = diskretisasi sudut  

Kompleksitas:

$$
O(N \cdot T)
$$

Resolusi sudut kecil → presisi tinggi → komputasi meningkat.

---

# 3. Studi Kasus 1 — Deteksi Marka Jalan

## Permasalahan

- Marka terputus  
- Bayangan kuat  
- Tekstur aspal kompleks  

Tujuan: mendeteksi garis dominan sebagai referensi arah kendaraan.

---

## Implementasi Lengkap

```python
import cv2
import numpy as np

img = cv2.imread('road.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5,5), 0)
edges = cv2.Canny(blur, 50, 150)

lines = cv2.HoughLines(edges, 1, np.pi/180, 150)

line_img = img.copy()

if lines is not None:
    for rho, theta in lines[:,0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(line_img, (x1,y1), (x2,y2), (0,0,255), 2)

comparison = np.hstack((img, line_img))

cv2.imshow("Lane Detection - Hough Line", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Analisis Engineering

Threshold 150 menentukan minimum voting:

$$
A(\rho,\theta) \ge \tau
$$

Jika terlalu rendah:

- False positive meningkat  
- Noise ikut terdeteksi  

Jika terlalu tinggi:

- Marka tipis hilang  
- Estimasi sudut bias  

Deviasi sudut:

$$
\Delta\theta
$$

menghasilkan error lintasan:

$$
e \approx L\tan(\Delta\theta)
$$

---

# 4. Hough Transform untuk Lingkaran

Persamaan lingkaran:

$$
(x-a)^2 + (y-b)^2 = r^2
$$

Ruang parameter:

$$
(a,b,r)
$$

Kompleksitas:

$$
O(N \cdot R)
$$

---

# Studi Kasus 2 — Inspeksi Diameter Pipa

```python
import cv2
import numpy as np

img = cv2.imread('pipe.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_blur = cv2.medianBlur(gray, 5)

circles = cv2.HoughCircles(
    gray_blur,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=50,
    param1=100,
    param2=30,
    minRadius=20,
    maxRadius=120
)

circle_img = img.copy()

if circles is not None:
    circles = np.uint16(np.around(circles))
    for c in circles[0,:]:
        center = (c[0], c[1])
        radius = c[2]
        cv2.circle(circle_img, center, radius, (0,255,0), 2)

comparison = np.hstack((img, circle_img))

cv2.imshow("Pipe Inspection - Hough Circle", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Analisis Parameter

### dp

Jika:

$$
dp > 1
$$

maka resolusi accumulator lebih rendah → komputasi ringan → presisi pusat menurun.

### minDist

Mengontrol jarak minimum antar pusat.

### param1

Threshold Canny internal.

### param2

Threshold voting:

$$
A(a,b,r) \ge \tau
$$

---

## Analisis Engineering Pengukuran

Jika radius terdeteksi:

$$
r_d
$$

dan referensi:

$$
r_0
$$

maka error diameter:

$$
\Delta D = 2(r_d - r_0)
$$

Kesalahan parameter dapat menyebabkan false reject atau false accept dalam quality control.

---

# 5. Studi Kasus 3 — Koreksi Kemiringan Dokumen

```python
import cv2
import numpy as np

img = cv2.imread('document.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

angles = []

if lines is not None:
    for rho, theta in lines[:,0]:
        angle = theta - np.pi/2
        angles.append(angle)

if len(angles) > 0:
    mean_angle = np.mean(angles)
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2,h//2),
                                mean_angle*180/np.pi,
                                1)
    rotated = cv2.warpAffine(img, M, (w,h))
else:
    rotated = img.copy()

comparison = np.hstack((img, rotated))

cv2.imshow("Document Deskew", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# Ringkasan Engineering

Hough Transform adalah metode voting pada ruang parameter untuk mendeteksi bentuk parametrik global.

Keunggulan:

- Robust terhadap fragmentasi  
- Stabil pada noise moderat  

Keterbatasan:

- Kompleksitas meningkat dengan dimensi parameter  
- Sensitif terhadap threshold dan resolusi  

Desain sistem harus mempertimbangkan:

- Target FPS  
- Variansi noise  
- Toleransi pengukuran  
- Integrasi dengan tahap lanjutan seperti tracking, OCR, dan metrologi industri  

---

# Mini Project Lanjutan

1. Lane detection real-time berbasis video  
2. Pengukuran diameter otomatis pada conveyor  
3. Deteksi rel kereta dari citra drone  
4. Analisis kemiringan panel surya  
5. Integrasi Hough + YOLO untuk validasi bentuk  
6. Evaluasi sensitivitas threshold terhadap noise Gaussian  
7. Sistem inspeksi botol berbasis lingkaran  
8. Analisis retakan beton menggunakan Hough Line  

---