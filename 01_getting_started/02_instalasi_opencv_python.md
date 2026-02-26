# 2. Instalasi OpenCV-Python

> Target pembahasan:
> - Cara instalasi pada Windows
> - Cara instalasi pada Linux/Ubuntu
> - Tes keberhasilan instalasi


Ada beberapa sistem operasi yang sering digunakan di Indonesia, yaitu Windows, Linux dan Mac. Nah, kita akan menjelaskan dasar instalasinya.


## - Instalasi pada Windows

1. Download Python 3.11.x dari situs resmi:
   https://www.python.org/downloads/

2. Unduh installer Windows x86-64 terbaru yang stabil.

3. Double klik file installer tersebut, dan jangan lupa beri tanda centang pada:
   **Add Python to PATH**

4. Lanjutkan proses instalasi hingga selesai.

5. Setelah instalasi selesai, buka Terminal atau Command Prompt.

6. Masuk ke folder project Anda, lalu buat virtual environment:

   ```
   python -m venv venv
   ```

7. Aktifkan virtual environment:

   ```
   venv\Scripts\activate
   ```

8. Install OpenCV dan dependency yang diperlukan:

   ```
   pip install opencv-contrib-python numpy matplotlib
   ```

9. Pastikan instalasi berhasil dengan mengecek versi:

   ```
   python -c "import cv2; print(cv2.__version__)"
   ```


## - Instalasi pada Ubuntu/Linux

1. Pastikan Python 3.11 sudah terinstall:

   ```
   python3 --version
   ```

2. Jika belum tersedia, install sesuai distribusi Linux yang digunakan.

3. Buat virtual environment:

   ```
   python3 -m venv venv
   ```

4. Aktifkan virtual environment:

   ```
   source venv/bin/activate
   ```

5. Install OpenCV:

   ```
   pip install opencv-contrib-python numpy matplotlib
   ```


## - Instalasi pada Mac

1. Install Python 3.11 dari python.org atau menggunakan Homebrew:

   ```
   brew install python@3.11
   ```

2. Buat virtual environment:

   ```
   python3 -m venv venv
   ```

3. Aktifkan virtual environment:

   ```
   source venv/bin/activate
   ```

4. Install OpenCV:

   ```
   pip install opencv-contrib-python numpy matplotlib
   ```


## - Test instalasi kalian

Setelah semua proses instalasi selesai, lakukan pengujian dengan membuat file Python baru dan jalankan kode berikut:

```python
import cv2

print("OpenCV version:", cv2.__version__)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

Jika kamera terbuka dan versi OpenCV tampil di terminal, maka instalasi berhasil.

Tekan tombol `q` untuk keluar dari program.