# 2.4 Interaksi Mouse dan Trackbar pada OpenCV

Bab ini membahas bagaimana OpenCV menangani interaksi pengguna melalui mouse dan trackbar. Pada tahap pengembangan sistem computer vision, fitur ini sangat penting untuk:

- Kalibrasi parameter
- Penentuan ROI (Region of Interest)
- Anotasi dataset
- Eksperimen threshold secara real-time
- Validasi algoritma sebelum otomatisasi penuh

---

# 2.4.1 Interaksi Mouse

> Target pembelajaran:
> - Memahami event-driven programming pada OpenCV
> - Menggunakan callback function
> - Menggambar objek berdasarkan interaksi mouse
> - Mengimplementasikan tool interaktif sederhana

---

## Teori Dasar (Konseptual)

OpenCV menggunakan pendekatan event-driven programming untuk menangani interaksi mouse.

Ketika suatu event terjadi (misalnya klik kiri), OpenCV memanggil fungsi callback yang telah kita daftarkan.

Event yang umum digunakan:

- `cv2.EVENT_LBUTTONDOWN`
- `cv2.EVENT_LBUTTONUP`
- `cv2.EVENT_RBUTTONDOWN`
- `cv2.EVENT_MOUSEMOVE`
- `cv2.EVENT_LBUTTONDBLCLK`

Setiap event memiliki informasi:

- Koordinat `(x, y)`
- Flags tambahan (misalnya tombol tambahan ditekan)

---

## Struktur Callback Function

```python
def fungsi_mouse(event, x, y, flags, param):
    pass
```

Parameter:

- `event` → jenis event
- `x, y` → posisi mouse
- `flags` → kondisi tambahan
- `param` → parameter tambahan (opsional)

Mendaftarkan callback:

```python
cv2.setMouseCallback("NamaWindow", fungsi_mouse)
```

---

## Contoh Dasar — Menampilkan Koordinat Klik

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

Setiap klik kiri akan menampilkan koordinat pada terminal.

---

## Contoh Dasar — Menggambar Lingkaran Saat Klik

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

---

## Studi Kasus Teknik — Tool Pengukuran Jarak Piksel

Dalam dunia teknik, sering diperlukan pengukuran jarak berbasis piksel sebelum dikonversi ke satuan nyata.

Contoh berikut memungkinkan pengguna memilih dua titik dan menghitung jaraknya.

```python
import cv2
import math

img = cv2.imread("anu.jpeg")
points = []

def hitung_jarak(event, x, y, flags, param):
    global points, img

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

        if len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]

            jarak = math.sqrt((x2-x1)**2 + (y2-y1)**2)

            cv2.line(img, points[0], points[1], (0,255,0), 2)
            cv2.putText(img, f"{int(jarak)} px",
                        (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255,0,0), 2)

            print("Jarak piksel:", jarak)
            points = []

        cv2.imshow("Kalibrasi", img)

cv2.imshow("Kalibrasi", img)
cv2.setMouseCallback("Kalibrasi", hitung_jarak)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

Digunakan untuk:

- Kalibrasi kamera
- Pengukuran panjang objek
- Analisis retakan struktur
- Pengukuran dimensi benda kerja

---

# 2.4.2 Trackbar

> Target pembelajaran:
> - Membuat slider parameter
> - Mengatur threshold secara real-time
> - Eksperimen parameter interaktif

---

## Teori Dasar Trackbar

Trackbar digunakan untuk mengubah parameter secara real-time tanpa mengubah kode.

Struktur dasar:

```python
cv2.createTrackbar(trackbar_name, window_name, value, max_value, callback)
```

Parameter:

- `trackbar_name` → nama slider
- `window_name` → window tempat slider muncul
- `value` → nilai awal
- `max_value` → nilai maksimum
- `callback` → fungsi ketika nilai berubah

---

## Contoh Dasar — Threshold Interaktif

```python
import cv2

def nothing(x):
    pass

img = cv2.imread("anu.jpeg", 0)

cv2.namedWindow("Threshold")
cv2.createTrackbar("Nilai", "Threshold", 0, 255, nothing)

while True:
    val = cv2.getTrackbarPos("Nilai", "Threshold")
    _, thresh = cv2.threshold(img, val, 255, cv2.THRESH_BINARY)

    cv2.imshow("Threshold", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
```

---

## Studi Kasus Teknik — Kalibrasi Threshold Sistem Inspeksi

Dalam sistem inspeksi visual industri, threshold tidak selalu konstan. Perubahan pencahayaan dapat mempengaruhi hasil segmentasi.

Trackbar memungkinkan engineer:

- Menguji nilai threshold
- Menentukan batas optimal
- Mengurangi kesalahan segmentasi

Trackbar sering digunakan sebelum sistem menggunakan adaptive threshold otomatis.

---

# Ringkasan Bab 2.4

1. OpenCV mendukung event-driven programming.
2. Mouse event menggunakan callback function.
3. Koordinat `(x, y)` penting untuk ROI.
4. Event dapat digunakan untuk anotasi dataset.
5. Berguna dalam kalibrasi kamera.
6. Dapat digunakan untuk pengukuran piksel.
7. Trackbar memungkinkan eksperimen parameter.
8. Berguna untuk threshold tuning.
9. Membantu debugging segmentasi.
10. Penting dalam prototyping sistem vision.
11. Digunakan dalam labeling data manual.
12. Digunakan dalam validasi bounding box.
13. Digunakan dalam kalibrasi warna.
14. Mengurangi trial-error di kode.
15. Fondasi pembuatan tool vision interaktif.

---

# Ide Mini Project

1. Tool pengukur panjang berbasis klik.
2. Sistem anotasi bounding box manual.
3. Kalibrasi threshold untuk deteksi retakan.
4. Tool cropping ROI interaktif.
5. Sistem penentuan area aman robot.
6. Simulator segmentasi interaktif.
7. Tool kalibrasi warna HSV.
8. Sistem penghitungan luas berbasis klik titik.
9. Dashboard tuning parameter real-time.
10. Prototype labeling dataset sederhana.