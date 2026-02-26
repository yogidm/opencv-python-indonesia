# 3. Memulai Fitur GUI pada OpenCV

## 3.1. Menggunakan Citra Digital

> Target pembahasan:
> - Dapat membaca citra dari sebuah file citra digital
> - Dapat menulis citra hasil pengolahan
> - Menampilkan citra pada jendela menggunakan fitur GUI OpenCV
> - Menggunakan keyboard event


### - Membaca Citra Digital

Citra digital dapat kita panggil pada proyek Python kita menggunakan fungsi `cv2.imread()`. Untuk pembacaan citra, file gambar sebaiknya berada pada direktori yang sama dengan file Python yang digunakan.

Untuk isian dari parameter kedua (flag), dapat digunakan:

- `cv2.IMREAD_COLOR` atau `1` → membaca citra berwarna (format BGR)
- `cv2.IMREAD_GRAYSCALE` atau `0` → membaca citra keabuan
- `cv2.IMREAD_UNCHANGED` atau `-1` → membaca citra tanpa perubahan (termasuk alpha channel)

Contoh kode:

```python
import cv2

# Panggil citra digital dengan nama anu.jpeg
img = cv2.imread("anu.jpeg", 0)
```

Pastikan file `anu.jpeg` berada pada folder yang sama dengan file `.py` Anda.

Jika kode dijalankan, belum akan muncul tampilan apapun sampai kita menggunakan fungsi GUI.


### - Menampilkan Citra Digital

Untuk menampilkan citra, gunakan fungsi `cv2.imshow()`.

```python
cv2.imshow('Gambar', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Penjelasan:

- `cv2.imshow()` → menampilkan citra pada jendela
- `cv2.waitKey(0)` → menunggu input keyboard tanpa batas waktu
- `cv2.destroyAllWindows()` → menutup seluruh jendela yang aktif


### - Menyimpan gambar menjadi sebuah file

Untuk menyimpan citra hasil pengolahan, gunakan:

```python
cv2.imwrite('hasil.png', img)
```

File akan tersimpan pada direktori yang sama dengan file Python.

Jika citra berbentuk biner, format `.bmp` disarankan agar tidak terjadi kompresi lossy.


### - Gabungkan semua kodenya

Berikut contoh lengkap membaca, memproses, dan menyimpan citra:

```python
import cv2

img = cv2.imread("anu.jpeg", 0)

imb = img.copy()
imb[imb > 100] = 255
imb[imb < 100] = 0

cv2.imshow('Gambar', img)
cv2.imshow('Gambar BW', imb)

k = cv2.waitKey(0)

if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('hasil_asli.png', img)
    cv2.imwrite('hasil_biner.bmp', imb)
    cv2.destroyAllWindows()
```

Tekan `ESC` untuk keluar tanpa menyimpan.  
Tekan `s` untuk menyimpan hasil.


---

## 3.2. Menggunakan Video

> Target pembelajaran:
> - Mengetahui pembacaan video dari file menggunakan `cv2.VideoCapture()`
> - Mengetahui pembacaan video dari kamera
> - Mengetahui proses menyimpan video menggunakan `cv2.VideoWriter()`

Video adalah kumpulan frame citra yang ditampilkan berurutan. Biasanya video memiliki 24–30 frame per second (FPS).


### - Membaca Video dari direktori lokal

```python
import cv2

cap = cv2.VideoCapture('video_ori.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Frame Ori', frame)
    cv2.imshow('Frame Gray', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```


### - Menggunakan capture webcam

Webcam internal biasanya memiliki address `0`.

```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Frame Ori', frame)
    cv2.imshow('Frame Gray', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```


### - Mengatur resolusi kamera

```python
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height
```


### - Menyimpan hasil capture menjadi video

Untuk menyimpan hasil video:

```python
import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('keluaran.mp4', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    out.write(frame)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
```

Catatan: Proses ini hanya menyimpan video (frame), tidak termasuk audio.


---

## 3.3. Menggunakan Fungsi Drawing

> Target pembelajaran:
> - Mengetahui fungsi dasar menggambar menggunakan OpenCV
> - Menggunakan fungsi `cv2.line()`, `cv2.circle()`, `cv2.rectangle()`, `cv2.putText()`, dll.

Fungsi drawing biasanya digunakan untuk memberi anotasi pada citra hasil pengolahan.

Parameter umum:

- `img` → frame tempat menggambar
- `color` → format BGR, misal `(0,255,0)`
- `thickness` → ketebalan garis (gunakan `-1` untuk fill)
- `lineType` → tipe garis

Contoh:

```python
import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)

cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 2)
cv2.rectangle(img, (100, 100), (300, 300), (0, 255, 0), 2)
cv2.circle(img, (256, 256), 50, (0, 0, 255), -1)
cv2.putText(img, 'OpenCV', (150, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2)

cv2.imshow('Drawing', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Untuk dokumentasi lengkap parameter drawing, silakan lihat dokumentasi resmi OpenCV.