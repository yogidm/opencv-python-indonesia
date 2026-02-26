# Transformasi Geometris pada Citra

> Target pembelajaran:
> - Memahami konsep transformasi geometris
> - Melakukan scaling, translasi, rotasi
> - Menggunakan affine dan perspective transform


Transformasi geometris digunakan untuk mengubah posisi, ukuran, atau orientasi citra tanpa mengubah informasi pixel secara langsung.


---

## 1. Scaling (Perubahan Ukuran)

Scaling digunakan untuk memperbesar atau memperkecil citra.

```python
import cv2

img = cv2.imread("anu.jpeg")

# Perbesar 2x
resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

cv2.imshow("Scaling", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Parameter penting:
- `fx` → skala sumbu x
- `fy` → skala sumbu y
- `interpolation` → metode interpolasi

Metode interpolasi umum:
- `cv2.INTER_NEAREST`
- `cv2.INTER_LINEAR`
- `cv2.INTER_CUBIC`
- `cv2.INTER_AREA`


---

## 2. Translasi (Pergeseran)

Translasi menggeser citra ke arah tertentu.

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

rows, cols = img.shape[:2]

M = np.float32([[1, 0, 100],
                [0, 1, 50]])

translated = cv2.warpAffine(img, M, (cols, rows))

cv2.imshow("Translasi", translated)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Penjelasan:
- 100 → geser ke kanan
- 50 → geser ke bawah


---

## 3. Rotasi

Rotasi dilakukan menggunakan matriks rotasi.

```python
import cv2

img = cv2.imread("anu.jpeg")

rows, cols = img.shape[:2]

M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)

rotated = cv2.warpAffine(img, M, (cols, rows))

cv2.imshow("Rotasi", rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Parameter:
- Titik pusat rotasi
- Sudut (derajat)
- Skala


---

## 4. Affine Transformation

Transformasi affine mempertahankan garis sejajar.

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

rows, cols = img.shape[:2]

pts1 = np.float32([[50,50], [200,50], [50,200]])
pts2 = np.float32([[10,100], [200,50], [100,250]])

M = cv2.getAffineTransform(pts1, pts2)

affine = cv2.warpAffine(img, M, (cols, rows))

cv2.imshow("Affine", affine)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Hanya membutuhkan 3 titik korespondensi.


---

## 5. Perspective Transformation

Perspective transform digunakan untuk mengubah sudut pandang (misalnya koreksi dokumen).

```python
import cv2
import numpy as np

img = cv2.imread("anu.jpeg")

rows, cols = img.shape[:2]

pts1 = np.float32([[56,65], [368,52], [28,387], [389,390]])
pts2 = np.float32([[0,0], [300,0], [0,300], [300,300]])

M = cv2.getPerspectiveTransform(pts1, pts2)

perspective = cv2.warpPerspective(img, M, (300,300))

cv2.imshow("Perspective", perspective)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Perspective transform membutuhkan 4 titik korespondensi.


---

## Ringkasan

- Scaling → `cv2.resize()`
- Translasi & Rotasi → `cv2.warpAffine()`
- Affine transform → 3 titik
- Perspective transform → 4 titik
- Semua transformasi berbasis matriks

Transformasi geometris sangat penting dalam:
- Data augmentation
- Koreksi perspektif
- Registrasi citra
- Preprocessing sebelum deteksi objek