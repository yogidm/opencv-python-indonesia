# OpenCV Python Indonesia

Repositori ini merupakan materi pembelajaran **Computer Vision menggunakan OpenCV (Python)** yang disusun secara sistematis untuk mahasiswa teknik dan praktisi.

Materi disusun dari konsep dasar hingga topik lanjutan dengan pendekatan:

- Teori matematis yang kuat
- Implementasi Python yang self-contained
- Visualisasi before–after bersandingan
- Analisis engineering mendalam
- Studi kasus lapangan

---

# 📚 Daftar Isi

## 1️⃣ Getting Started
- [Pengenalan OpenCV](01_getting_started/01_pengenalan_opencv.md)
- [Instalasi OpenCV Python](01_getting_started/02_instalasi_opencv_python.md)

---

## 2️⃣ GUI dan Input
- [GUI Dasar](02_gui_dan_input/01_gui_dasar.md)
- [Mouse dan Trackbar](02_gui_dan_input/02_mouse_dan_trackbar.md)

---

## 3️⃣ Image Processing

- [Operasi Dasar Citra](03_image_processing/01_operasi_dasar_citra.md)
- [Transformasi Geometris](03_image_processing/02_transformasi_geometris.md)
- [Pengambangan Citra (Thresholding)](03_image_processing/03_pengambangan_citra.md)
- [Penghalusan Citra (Smoothing)](03_image_processing/04_penghalusan_citra.md)
- [Morfologi Citra](03_image_processing/05_morfologi.md)

---

## 4️⃣ Advanced Processing
*(Coming Soon)*

---

## 5️⃣ Feature Detection
*(Coming Soon)*

---

## 6️⃣ Video Analysis
*(Coming Soon)*

---

## 7️⃣ 3D Vision
*(Coming Soon)*

---

## 8️⃣ Object Detection
*(Coming Soon)*

---

# 🧠 Filosofi Materi

Materi ini tidak hanya mengajarkan penggunaan fungsi OpenCV, tetapi:

- Representasi matematis citra
- Distribusi intensitas dan histogram
- Separability dan variansi antar kelas
- Operasi morfologi berbasis teori himpunan
- Transformasi homogen dan warping
- Analisis topologi objek

Tujuannya adalah membentuk pemahaman konseptual yang kuat, bukan sekadar pengguna library.

---

# ⚙️ Prasyarat

- Python 3.x
- OpenCV (`pip install opencv-python`)
- NumPy
- scikit-image (untuk Sauvola)

---

# 🧪 Format Kode

Semua contoh:

- Self-contained
- Dapat langsung dijalankan
- Menggunakan visualisasi bersandingan
- Tidak bergantung pada variabel sebelumnya

---

# 📌 Target Pembaca

- Mahasiswa Teknik Informatika
- Mahasiswa Teknik Elektro
- Peneliti Computer Vision
- Praktisi sistem vision industri

---

# 🚀 Roadmap

- Edge detection
- Frequency domain filtering
- Feature extraction (SIFT, ORB)
- Camera calibration
- Homography dan epipolar geometry
- Deep learning integration

---

# 📜 Lisensi

Open-source untuk pembelajaran dan pengembangan akademik.



------------
# (lawas) Dasar OpenCV

OpenCV merupakan sebuah pustaka yang bersifat open source yang digunakan untuk berbagai pengolahan citra digital pada komputer.

Pada tutorial ini, akan dijelaskan tentang beberapa dokumentasi mengenai dasar-dasar penggunaan dan fitur dari OpenCV menggunakan bahasa pemograman python. Oleh karenanya, daftar isinya adalah sebagai berikut:

1. [Yuk mengenal OpenCV Python](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#1-yuk-mengenal-opencv-python)
    - [OpenCV-Python](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#--opencv-python)
    - [Tentang tutorial ini](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#--tentang-tutorial-ini)
    - [Apa saja kentungannya?](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#--apa-saja-keuntungannya)
    - [Ayo mulai belajar!](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#--ayo-mulai-belajar)
2. [Instalasi OpenCV-Python](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#2-instalasi-opencv-python)
    - [Instalasi pada Ubuntu](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#--instalasi-pada-ubuntulinux)
    - [Instalasi pada Windows](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#--instalasi-pada-windows)
    - [Tes Instalasi Kalian](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#--test-instalasi-kalian)
3. [Memulai Fitur GUI OpenCV](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#3-memulai-fitur-gui-pada-opencv)
    - [Menggunakan Citra Digital](https://github.com/yogidm/opencv-python-indonesia/blob/master/opencv-python-indonesia.md#--menggunakan-citra-digital)
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
Testing sync VS Code