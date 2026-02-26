# Operasi Dasar Citra Digital

> Target pembelajaran:
> - Memahami representasi citra sebagai array
> - Mengakses dan memodifikasi nilai pixel
> - Menggunakan ROI (Region of Interest)
> - Melakukan operasi aritmetika dasar pada citra


## 1. Representasi Citra sebagai Array

Pada OpenCV, citra direpresentasikan sebagai array NumPy.

- Citra grayscale → matriks 2D
- Citra berwarna → matriks 3D (BGR)

Contoh:

```python
import cv2

img = cv2.imread("anu.jpeg")
print(type(img))
print(img.shape)
```

Output `shape` untuk citra berwarna biasanya:

```
(tinggi, lebar, 3)
```


---

## 2. Mengakses dan Mengubah Pixel

Untuk membaca nilai pixel:

```python
import cv2

img = cv2.imread("anu.jpeg")

pixel = img[100, 200]
print("Nilai pixel:", pixel)
```

Format warna adalah BGR (Blue, Green, Red).

Untuk mengubah pixel:

```python
img[100, 200] = [0, 255, 0]  # warna hijau
```

Untuk grayscale:

```python
gray = cv2.imread("anu.jpeg", 0)
gray[100, 200] = 255
```


---

## 3. Region of Interest (ROI)

ROI digunakan untuk mengambil bagian tertentu dari citra.

```python
import cv2

img = cv2.imread("anu.jpeg")

roi = img[100:300, 200:400]

cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

ROI sangat berguna dalam:
- Deteksi objek
- Cropping
- Feature extraction


---

## 4. Operasi Aritmetika Dasar pada Citra

### a. Penjumlahan Citra

```python
import cv2
import numpy as np

img1 = cv2.imread("anu.jpeg")
img2 = cv2.imread("anu.jpeg")

hasil = cv2.add(img1, img2)

cv2.imshow("Hasil", hasil)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Gunakan `cv2.add()` agar nilai pixel tetap dalam rentang 0–255.


### b. Pengurangan Citra

```python
hasil = cv2.subtract(img1, img2)
```


### c. Blending (Penggabungan dengan Bobot)

```python
blend = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)
```

Parameter:
- 0.7 → bobot citra pertama
- 0.3 → bobot citra kedua
- 0 → gamma (bias)


---

## 5. Operasi Bitwise

Operasi bitwise sering digunakan untuk masking.

### a. AND

```python
mask = cv2.imread("mask.png", 0)
hasil = cv2.bitwise_and(img1, img1, mask=mask)
```

### b. OR

```python
hasil = cv2.bitwise_or(img1, img2)
```

### c. NOT

```python
hasil = cv2.bitwise_not(img1)
```

Operasi ini banyak digunakan dalam segmentasi dan manipulasi area tertentu.


---

## 6. Mengetahui Performa Operasi

Untuk mengukur waktu eksekusi:

```python
import cv2
import time

img = cv2.imread("anu.jpeg")

start = time.time()

for i in range(1000):
    _ = cv2.GaussianBlur(img, (5,5), 0)

end = time.time()

print("Waktu eksekusi:", end - start)
```

Alternatif lain dapat menggunakan `cv2.getTickCount()` dan `cv2.getTickFrequency()` untuk presisi lebih tinggi.


---

## Ringkasan

- Citra adalah array NumPy.
- Pixel dapat diakses dengan indeks `[y, x]`.
- ROI memudahkan manipulasi area tertentu.
- Gunakan fungsi OpenCV seperti `cv2.add()` untuk menjaga stabilitas nilai pixel.
- Operasi bitwise penting untuk masking.
- Pengukuran performa penting dalam aplikasi real-time.

Operasi dasar ini menjadi fondasi untuk seluruh teknik pengolahan citra lanjutan.