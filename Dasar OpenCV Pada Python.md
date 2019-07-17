
# Dasar OpenCV

OpenCV merupakan sebuah pustaka yang bersifat open source yang digunakan untuk berbagai pengolahan citra digital pada komputer. [sejarah opencv]

Pada tutorial ini, akan dijelaskan tentang beberapa dokumentasi mengenai dasar-dasar penggunaan dan fitur dari OpenCV menggunakan bahasa pemograman python. Oleh karenanya, daftar isinya adalah sebagai berikut:

1. Yuk mengenal OpenCV Python
    - Apa itu OpenCV
    - OpenCV-Python
    - Tentang tutorial ini
    - Apa saja kentungannya?
    - Ayo mulai belajar!
2. Instalasi OpenCV-Python
    - Instalasi pada Ubuntu
    - Instalasi pada Windows
3. Memulai Fitur GUI OpenCV
    - Menggunakan Citra Digital
    - Menggunakan Video
    - Menggunakan Fungsi Drawing
    - Menggunakan Interaksi Tetikus
    - Menggunakan Trackbar
4. Operasi Dasar Citra Digital
    - Menggunakan Pixel, ROI, dan lainnya
    - Perhitungan Aritmetika Dasar Pada Citra
    - Mengetahui Performa Operasi Pada Citra
5. Pengolahan Citra pada OpenCV
    - Mengubah Ruang Warna
    - Transformasi Geometris pada Citra
    - Pengambangan Citra
    - Penghalusan Citra
    - Transformasi Morfologi Citra
    - Gradasi Citra
    - Deteksi Tepi 
    - Citra Piramida
    - Contour Pada OpenCV
    - Histogram 
    - Transformasi Fourier, dsb
    - Pencocokan Pola
    - Hough Line Transform
    - Hough Circle Transform
    - Penggolongan Watershed Algorithm
    - Algoritma GrabCut pada OpenCV
6. Deteksi Fitur dan Description
    - Memahami Fitur pada Citra
    - Deteksi Pojok - Harris
    - Deteksi Pojok dan Fitur yang baik untuk dikenali - Shi-Tomasi
    - Memahami SIFT (Scale-Invariant Feature Transform)
    - Memahamu SURF (Speeded-Up Robust Feature)
    - Algoritma FAST dan Deteksi Pojok
    - BRIEF (Binary Robust Independent Elementary Feature)
    - ORB (Oriented FAST and Rotated BRIEF)
    - Feature Matching
    - Feature Matching + Homography to find object
7. Analisa Video
    - Meanshift dan Camshift
    - Optical FLow
    - Background Subtraction
8. Kalibrasi Kamera dan Rekonstruksi 3D
    - Kalibrasi Kamera
    - Estimasi Pose
    - Epipolar Geometri
    - Kedalaman dari citra Stereo
9. Deteksi Objek
    - Deteksi Wajah
    
    
    
`update : 17 Juli 2019`

# 1. Yuk mengenal OpenCV Python

<b>OpenCV</b> (open source computer vision) merupakan sebuah pustaka bahasa pemograman yang ditujukan untuk penggunaan pengolahan citra secara waktu nyata. Secara original, OpenCV dikembangkan oleh Intel, kemudian didukung oleh [Willow Garage](https://en.wikipedia.org/wiki/Willow_Garage) dan kemudian Itseez (yang diakuisisi oleh Intel). Pustaka OpenCV sudah mendukung lintas platform dan dapat digunakan dengan gratis untuk digunakan di bawah [lisensi BSD](https://en.wikipedia.org/wiki/BSD_licenses) Open-source. Dalam perkembangannnya, OpenCV sudah mendukung beberapa framework untuk [deep-learning](https://en.wikipedia.org/wiki/Deep_learning) seperti [TensorFlow](https://en.wikipedia.org/wiki/TensorFlow), [YOLO](https://pjreddie.com/darknet/yolo/), [Torch/PyTorch](https://en.wikipedia.org/wiki/PyTorch) dan [Caffee](https://en.wikipedia.org/wiki/Caffe_(software)). Beberapa model terbaru yang mendukung ada pada [daftar berikut ini](https://docs.opencv.org/master/d2/d58/tutorial_table_of_content_dnn.html). 

## - OpenCV-Python

Ya, pada tutorial kali ini, kita akan menggunakan Python untuk membahas OpenCV-nya. Jadi, jika kalian masih belum paham atau pengen belajar tentang Python, bisa membaca tutorial Dasar Python sebelumnya pada [tautan berikut](https://github.com/yogidm/Dasar-Python). *) jangan lupa untuk di-star ya repo nya...

Mengapa Python? kurang lebih karena bahasa Python lebih mudah dibaca dalam Bahasa Inggris. Selain itu, juga lumayan cepat dalam komputasinya, meski tak secepat bahasa C++. Akan tetapi, dari kemudahan terbacanya tersebut, dapat memudahkan pembelajar untuk memahaminya. Jadi, tetap semangat ya untuk belajar hal yang mungkin baru. 

Untuk Python yang akan digunakan pada tutorial ini adalah versi `Python 3.6.x` sedangkan untuk OpenCV nya digunakan `OpenCV 4.1.x`

## - Tentang tutorial ini

Tutorial ini ditujukan untuk kalian yang baru atau belum penah memahami OpenCV sebagai sebuah pustaka pada bahasa pemograman. Oleh karenanya, tutorial ini berisi tentang sedikit teori dasar dari pengolahan citra digital yang nantinya akan diberi tutorial penggunaannya menggunakan pustaka OpenCV. Ya, setidaknya kalian sudah membaca bagaimana toeri yang sebenarnya terjadi pada tiap pustaka dan fungsinya. Kebanyakan pada pustaka OpenCV hanya disediakan fungsi-fungsi yang sudah jadi saja. Selain itu, pada akhir pembahasan tiap bab nya, akan kami sematkan sebuah video yang bisa kalian gunakan sebagai suplemen atau patokan tutorialnya bekerja. 

Apabila kalian mengalami permasalahan pada contoh kode yang disematkan atau ingin berkontribusi pada Tutorial Dasar OpenCV ini, kalian bisa email kami pada de.mhnd[at]gmail[dot]com

## - Apa saja keuntungannya?

Keuntungannya mungkin tidak ada selain hanya sharing ilmu tentang OpenCV menggunakan Pyhton. Jadi, kalian bisa menggunakan ilmu yang ada didalamnya untuk kebutuhan kalian pribadi atau yang lainnya. tetapi bukan tulisannya ya... lantas kalian langsung menduplikat semua atau sebagian isi dari tutorial ini untuk dibuat buku, skripsi, atau laporan kalian. Bukan begitu cara mainnya. Kami hanya membagi ilmu ini dalam Bahasa Indonesia. 

`Sharing is Caring`. 

## - Ayo mulai belajar!

Langkah pertama yang bisa kalian buat adalah membuat akun [github](https://github.com/) dan mem-fork atau star tutorial ini agar kalian mudah mencari atau kalian bisa bookmark tutorial ini pada browser kalian. 

### Contributor
- [yogidm](https://github.com/yogidm)


# 2. Instalasi OpenCV-Python

Ada beberapa sistem operasi yang sering digunakan di Indonesia, yaitu Windows, Linux dan Mac. Nah, kita akan menjelaskan dasar instalasinya. 

## - Instalasi pada Windows

- Download Python 3.6.x pada tautan [berikut](https://www.python.org/downloads/release/python-368/) (Release Date: Dec. 24, 2018). Klik dan unduh `Windows x86-64 executable installer` pada daftar tabel di bagian bawah. 

<img src="Gambar/Instalasi_python_Win.png">

- Double klik file tersebut, dan jangan lupa beri tanda contreng pada <b>Add PATH Python 3.6.x</b>. lalu lanjutkan instalasi Python seperti biasanya. 
- Setelah sudah selesai proses instalasi, barulah kita mulai instalasi OpenCV. Masuk pada `command promt` Windows. `Crtl + R`, ketikkan `cmd`.
- Install opencv-python 4.1.x via pip dengan mengetikkan `pip3 install opencv-python`
- Numpy akan terinstall otomatis satu paket dengan instalasi opencv-python
- Jika instalasi keduanya berhasil, maka selesai dan siap untuk digunakan. Jika masih terjadi error, maka copy and paste errornya pada search engine. Semoga error tersebut ada di `stackoverflow` :D

## - Instalasi pada Ubuntu/Linux

Untuk instalasi pada Ubuntu/Linux, kalian bisa membuka terminal dengan menekan `Ctrl + Alt + T` dan memasukkan perintah berikut:

- Python 3.6.x `sudo apt-get install idle-python3.6`
- OpenCV-Python 4.1.x via pip3 `pip3 install opencv-python`
- Numpy sudah sepaket terinstall dengan OpenCV

## - Instalasi pada Mac

Nah, silahkan cari sendiri ya... Author belum pernah menggunakan mac, jadi kurang lebih sama dengan linux sepertinya. :D

## - Test instalasi kalian

Nah, apakah instalasi kalian sudah benar dan sukses? Kalian bisa membuat sebuah demo untuk mengakusisi citra dari kamera webcam kalian. 

- Buka `IDLE Using Python 3.6` sebagai editor Python kalian. 
- Buat `New File` 
- Masukkan kode berikut ini:

```python
import cv2
cap=cv2.VideoCapture(0)

while(True):
    ret,frame=cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
```

- Simpan dokumen tersebut sesuai keinginan kalian. 
- Run dengan menekan tombol `F5`.
- Kurang lebih akan menunjuukkan tampilan seperti gambar berikut ini. 

<img src="Gambar/Capture_camera.png">

- Tekan tombol `q` untuk keluar dari program capture kamera. 

Nah, setelah instalasi kalian sukses, mari kita lanjutkan pada bab selanjutnya. 


# 3. Memulai Fitur GUI pada OpenCV

## - Menggunakan Citra Digital

Citra digital dapat kita panggil pada proyek Python kita menggunakan fugnsi `c2.imread()`. Untuk pembacaan citra yang bisa dipanggil, hanya pada direktori yang sama dengan letak direktori dari dokumen Python itu disimpan. Jadi, jangan lupa memindah lokasi gambar yang akan digunakan pada folder yang sama dengan dokumen kalian ya... 

Untuk isian dari `flag` kedua fungsi tersebut, dapat digunakan:
- `cv2.IMREAD_COLOR` : atau `1` yang berartikan memanggil citra berwarna dengan 3 dimensi yaitu BGR. 
- cv2.IMREAD_GRAYSCALE : atau `0` yang memanggil citra dengan 1 dimensi atau citra keabuan
- cv2.IMREAD_UNCHANGED : atau `-1` yang memanggil citra tanpa adanya perubahan seperti citra dengan kanal alpha. 


Coba buat sebuah dokumen baru dan tuliskan kode berikut didalamnya. 

```python
import cv2

# Panggil citra digital dengan nama anu.jpeg
# dan memasukkannya pada variabel img
img = cv2.imread("anu.jpeg", 0)
```
untuk gambar `anu.jpeg` , kita dapat menggunakan gambar berikut. Silahkan unduh disini atau klik kanan gambar dibawah ini lalu `save image as`.

<img src="Gambar/anu.jpeg">

ketika dokumen tersebut sudah disimpan dengan satu direktori dengan gambar tersebut, apabila di `run` maka tidak akan ada tampilan gambar sama sekali hingga kita menampilkannya menggunakan fitur GUI dari OpenCV. 

## - Menampilkan Citra Digital

Menampilkan citra yang sudah dipanggil dan dirubah menjadi sebuah variabel, maka kita bisa menggunakan fungsi `cv2.imshow()` untuk menampilkan citra pada variabel tersebut. Untuk jendela untuk menampilkan citra, akan secara otomatis menyesuaikan dengan ukuran citranya. pada penulisan fungsinya, ada beberapa masukan, yaitu nama windownya dan diikuti dengan nama variabel yang berisikan citra yang akan ditampilkan. Coba kode berikut dibawah kode pembacaan citra digital diatas.

```python
cv2.imshow ('Gambar', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Apabila kalian menjalakan programnya, maka akan menampilkan gambar seperti berikut:

<img src="Gambar/Gambar_1.png">

pada baris `cv2.waitKey(0)` merupakan sebuah fungsi untuk menahan frame atau citra yang sedang kita gunakan. Dengan kata lain, apabila kita menggunakan banyak frame, kita tidak perlu menahannya dengan memberikan nilai selain `0`. 

pada baris `cv2.destroyAllWindows()` merupakan sebuah fungsi untuk menutup semua jendela yang aktif pada sebuah program yang berjalan. Biasanya kita bisa menggabungkan dengan perintah `jika tombol 'q' tertekan, maka tutup semua jendela` (seperti pada kode tes instalasi pada bab 2).

## - Menyimpan gambar menjadi sebuah file

Menyimpan gambar hasil pengolahan citra digital pada OpenCV dapat digunakan fungsi 
`cv2.imwrite()`. Untuk nama file, kalian bisa menggunakan `.png` atau `.jpg` atau sesuai dengan kebutuhan kalian. Jika hasil citra kalian dalam bentuk citra biner, gunakan format `.bmp` untuk hasil yang lebih baik. File akan disimpan pada direktori yang sama dengan letak dokumen disimpan. 

```python
cv2.imwrite('burung.png',img)
```

## - Gabungkan semua kodenya

Kode diatas merupakan kepingan kode yang memanggil dan menampilkannya pada jendela menggunakan fitur GUI pada OpenCV. Mari kita gabungkan kesemuanya. 

```python
import cv2

# Panggil citra digital dengan nama anu.jpeg
img = cv2.imread("anu.jpeg", 0)

imb = img.copy()
imb[imb>100]=255
imb[imb<100]=0

cv2.imshow ('Gambar', img)
cv2.imshow ('Gambar BW', imb)
k = cv2.waitKey(0)

if k == 27:         # menunggu hingga tombol ESC ditekan dan keluar
    cv2.destroyAllWindows()
elif k == ord('s'): # menunggu hingga tombol 's' ditekan dan simpan
    cv2.imwrite('burung.png',img)
    cv2.imwrite('burungBW.bmp',imb)
    cv2.destroyAllWindows()
```
Maka tampilan hasil ketika sudah disimpan akan seperti berikut ini. 

<img src="Gambar/Gambar_2.png">
