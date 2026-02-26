# 2. GUI dan Input pada OpenCV

Bab ini membahas bagaimana OpenCV menangani interaksi visual antara sistem dan pengguna. Pada tahap awal pengembangan sistem computer vision, GUI berfungsi sebagai antarmuka engineering untuk:

- Validasi algoritma
- Debugging
- Kalibrasi sistem
- Monitoring performa real-time

Sebelum sistem berjalan otomatis (headless), hampir semua sistem vision melewati fase GUI-based prototyping.

---

# 2.1 Menggunakan Citra Digital

> Target pembahasan:
> - Memahami representasi citra dalam memori
> - Membaca citra dari file
> - Menampilkan citra
> - Menyimpan hasil pengolahan
> - Menggunakan input keyboard

---

## Teori Dasar (Konseptual dan Teknis)

### Representasi Citra dalam Komputer

Citra digital disimpan sebagai matriks numerik. Dalam OpenCV (Python), citra direpresentasikan sebagai array NumPy dengan struktur:

```
(height, width, channels)
```

Untuk citra berwarna:
- Channels = 3 (BGR)

Untuk grayscale:
- Channels = 1

Contoh:
- Resolusi 640x480 grayscale → matriks 480x640
- Resolusi 640x480 warna → matriks 480x640x3

Setiap elemen matriks menyimpan intensitas piksel (0–255 untuk 8-bit).

OpenCV secara default menggunakan format **BGR**, bukan RGB.

---

### Mekanisme Pembacaan File

Ketika `cv2.imread()` dipanggil:

1. File dibaca dari storage.
2. Didekodekan sesuai format (JPEG, PNG, BMP).
3. Disimpan ke memori sebagai array.
4. Disiapkan untuk diproses.

Jika file tidak ditemukan → fungsi mengembalikan `None`.

---

## Struktur Fungsi

```
cv2.imread(filename, flag)
```

Parameter flag:

- `cv2.IMREAD_COLOR`
- `cv2.IMREAD_GRAYSCALE`
- `cv2.IMREAD_UNCHANGED`

Menampilkan citra:

```
cv2.imshow(window_name, image)
cv2.waitKey(delay)
cv2.destroyAllWindows()
```

---

## Teori Event Loop (Penting)

OpenCV GUI bekerja berdasarkan event loop sederhana:

1. `imshow()` menggambar frame ke buffer window.
2. `waitKey()` memproses event (keyboard input).
3. Jika `waitKey()` tidak dipanggil → window tidak responsif.

`waitKey(delay)`:
- delay = 0 → tunggu tanpa batas
- delay > 0 → tunggu dalam milidetik

---

## Contoh Dasar

```python
import cv2

img = cv2.imread("anu.jpeg", 0)

cv2.imshow("Gambar", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Menyimpan Citra

```python
cv2.imwrite("hasil.png", img)
```

Saat menyimpan:
- JPEG → kompresi lossy
- PNG → kompresi lossless
- BMP → tanpa kompresi

Untuk citra biner → BMP lebih stabil.

---

## Contoh Lengkap

```python
import cv2

img = cv2.imread("anu.jpeg", 0)

imb = img.copy()
imb[imb > 100] = 255
imb[imb < 100] = 0

cv2.imshow("Asli", img)
cv2.imshow("Biner", imb)

k = cv2.waitKey(0)

if k == 27:
    cv2.destroyAllWindows()
elif k == ord("s"):
    cv2.imwrite("hasil_asli.png", img)
    cv2.imwrite("hasil_biner.bmp", imb)
    cv2.destroyAllWindows()
```

---

# 2.2 Menggunakan Video

> Target pembelajaran:
> - Memahami arsitektur akuisisi video
> - Memahami konsep frame buffer
> - Membaca video dari file
> - Menggunakan webcam
> - Menyimpan video hasil proses

---

## Teori Dasar Video (Teknis)

Video adalah aliran frame citra berurutan yang ditampilkan pada interval waktu tertentu.

Konsep penting:

### 1. Frame
Satu citra tunggal dalam urutan video.

### 2. FPS (Frame Per Second)
Jumlah frame yang diproses per detik.
- 30 FPS → 1 frame setiap ~33 ms

### 3. Buffer
Ketika kamera aktif:
- Kamera menghasilkan frame
- Frame masuk ke buffer
- Program membaca buffer
- Buffer dibersihkan untuk frame berikutnya

Jika pembacaan lambat → frame bisa tertinggal.

---

## Arsitektur Akuisisi Video

1. Inisialisasi capture
2. Loop pembacaan frame
3. Pemrosesan frame
4. Visualisasi
5. Terminasi

---

## Struktur Fungsi

Membuka video/kamera:

```
cv2.VideoCapture(source)
```

Membaca frame:

```
ret, frame = cap.read()
```

Menutup capture:

```
cap.release()
```

---

## Contoh Dasar — Video File

```python
import cv2

cap = cv2.VideoCapture("video_ori.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Contoh Dasar — Webcam

```python
cap = cv2.VideoCapture(0)
```

Address `0` biasanya kamera utama.

---

## Mengatur Properti Kamera

Properti kamera dikontrol melalui ID numerik:

- 3 → width
- 4 → height
- 5 → FPS

```python
cap.set(3, 640)
cap.set(4, 480)
```

---

## Menyimpan Video

Video disimpan menggunakan encoder (FourCC).

```python
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("keluaran.mp4", fourcc, 20.0, (640, 480))
```

Audio tidak tersimpan karena OpenCV hanya memproses frame visual.

---

## Studi Kasus Teknik — Sistem Inspeksi Visual Industri

Pada sistem inspeksi kualitas:

- Kamera membaca objek pada conveyor
- Frame diproses (threshold, contour)
- Bounding box ditampilkan
- Area dihitung
- Sistem diuji secara real-time

```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Area: {int(area)}",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 0, 255), 2)

    cv2.imshow("Inspection System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

GUI berfungsi sebagai alat validasi sebelum sistem di-deploy.

---

# 2.3 Menggunakan Fungsi Drawing

Drawing digunakan untuk:

- Visualisasi hasil deteksi
- Memberi anotasi
- Debugging sistem

Parameter penting:

- `img`
- `color`
- `thickness`
- `lineType`

Contoh:

```python
import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)

cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 2)
cv2.rectangle(img, (100, 100), (300, 300), (0, 255, 0), 2)
cv2.circle(img, (256, 256), 50, (0, 0, 255), -1)
cv2.putText(img, "OpenCV", (150, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2)

cv2.imshow("Drawing", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# Ringkasan Bab 2

1. Citra adalah matriks numerik.
2. OpenCV menggunakan format BGR.
3. `imshow()` membutuhkan `waitKey()`.
4. Video adalah urutan frame.
5. FPS menentukan interval waktu frame.
6. Capture bekerja dengan buffer.
7. Frame diproses dalam loop.
8. Properti kamera dapat dikontrol.
9. VideoWriter menyimpan frame ke file.
10. Audio tidak disimpan.
11. GUI penting untuk prototyping.
12. Digunakan untuk debugging.
13. Digunakan dalam kalibrasi.
14. Digunakan dalam inspeksi industri.
15. Digunakan dalam monitoring keamanan.
16. Digunakan dalam pengukuran berbasis piksel.
17. Fondasi sebelum sistem otomatis.
18. Fondasi sebelum integrasi robotik.
19. Fondasi sebelum embedded deployment.
20. Tahap wajib dalam engineering workflow computer vision.

---

# Ide Mini Project

1. Penghitung objek pada conveyor.
2. Sistem monitoring parkir.
3. Tool anotasi dataset.
4. Pengukur jarak piksel.
5. Deteksi gerakan ruangan.
6. Monitoring kehadiran objek.
7. Visualisasi area robot.
8. Crop interaktif dataset.
9. Sistem inspeksi retakan sederhana.
10. Dashboard visual debugging vision system.