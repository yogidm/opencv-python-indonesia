# Interaksi Tetikus dan Trackbar pada OpenCV

## 1. Menggunakan Interaksi Tetikus (Mouse)

> Target pembelajaran:
> - Memahami event mouse pada OpenCV
> - Menggunakan callback function
> - Menggambar objek berdasarkan interaksi mouse


OpenCV menyediakan fungsi untuk menangkap event dari mouse menggunakan:

```
cv2.setMouseCallback()
```

Fungsi ini membutuhkan:
- Nama window
- Fungsi callback

Struktur dasar callback:

```python
def fungsi_mouse(event, x, y, flags, param):
    pass
```

Parameter:
- `event` → jenis event (klik kiri, klik kanan, dll.)
- `x, y` → koordinat posisi mouse
- `flags` → kondisi tambahan
- `param` → parameter tambahan (opsional)


### Contoh 1 — Menampilkan Koordinat Klik

```python
import cv2

def klik_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Koordinat:", x, y)

img = cv2.imread("anu.jpeg")
cv2.imshow("Gambar", img)
cv2.setMouseCallback("Gambar", klik_mouse)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

Setiap klik kiri akan menampilkan koordinat di terminal.


### Contoh 2 — Menggambar Lingkaran Saat Klik

```python
import cv2

img = cv2.imread("anu.jpeg")

def gambar_lingkaran(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 20, (0, 255, 0), -1)
        cv2.imshow("Gambar", img)

cv2.imshow("Gambar", img)
cv2.setMouseCallback("Gambar", gambar_lingkaran)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

Klik kiri akan menggambar lingkaran pada posisi mouse.


---

## 2. Menggunakan Trackbar

> Target pembelajaran:
> - Membuat slider interaktif
> - Mengontrol parameter secara real-time


Trackbar digunakan untuk membuat kontrol interaktif seperti slider.

Fungsi utama:

```
cv2.createTrackbar()
```

Struktur dasar:

```python
cv2.createTrackbar(nama_trackbar, nama_window, nilai_awal, nilai_maks, fungsi_callback)
```


### Contoh 1 — Trackbar Sederhana

```python
import cv2
import numpy as np

def nothing(x):
    pass

img = np.zeros((300, 512, 3), np.uint8)

cv2.namedWindow('Trackbar')
cv2.createTrackbar('R', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('G', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('B', 'Trackbar', 0, 255, nothing)

while True:
    r = cv2.getTrackbarPos('R', 'Trackbar')
    g = cv2.getTrackbarPos('G', 'Trackbar')
    b = cv2.getTrackbarPos('B', 'Trackbar')

    img[:] = [b, g, r]

    cv2.imshow('Trackbar', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
```

Trackbar di atas digunakan untuk mengubah warna background secara real-time.


---

## 3. Trackbar untuk Thresholding Citra

Contoh penggunaan trackbar untuk mengatur nilai threshold:

```python
import cv2

def nothing(x):
    pass

img = cv2.imread("anu.jpeg", 0)

cv2.namedWindow('Threshold')
cv2.createTrackbar('Nilai', 'Threshold', 0, 255, nothing)

while True:
    nilai = cv2.getTrackbarPos('Nilai', 'Threshold')

    _, thresh = cv2.threshold(img, nilai, 255, cv2.THRESH_BINARY)

    cv2.imshow('Threshold', thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
```

Dengan trackbar, pengguna dapat melihat perubahan threshold secara langsung tanpa mengubah kode.


---

## Ringkasan

- `cv2.setMouseCallback()` digunakan untuk menangani event mouse.
- `cv2.createTrackbar()` digunakan untuk membuat kontrol interaktif.
- Kombinasi keduanya sangat berguna untuk eksperimen parameter pengolahan citra secara real-time.

Interaksi ini sangat penting dalam tahap eksplorasi data dan tuning parameter pada computer vision.