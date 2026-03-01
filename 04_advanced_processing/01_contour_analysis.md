# 4.1 Contour Analysis (Analisis Kontur)

---

# 1. Posisi Kontur dalam Pipeline Computer Vision

Dalam sistem computer vision klasik, alur pemrosesan dapat dinyatakan sebagai:

Akuisisi → Preprocessing → Segmentasi → **Representasi Geometri (Contour)** → Ekstraksi Fitur → Decision System

Kontur adalah transformasi dari domain raster (piksel) menuju domain geometri (kurva diskret). Tahap ini mengubah representasi berbasis grid menjadi representasi berbasis batas (boundary representation).

Secara matematis, citra digital didefinisikan sebagai:

$$
I : \Omega \subset \mathbb{Z}^2 \rightarrow \mathbb{R}
$$

Setelah segmentasi diperoleh fungsi indikator:

$$
B(x,y) =
\begin{cases}
1 & \text{objek} \\
0 & \text{latar}
\end{cases}
$$

Boundary didefinisikan sebagai:

$$
\partial R = \{ p \in R \mid \exists q \in N(p) \text{ dengan } B(q)=0 \}
$$

Interpretasi engineering:

Kontur adalah piksel objek yang berbatasan langsung dengan latar. Secara fisik, ini ekuivalen dengan garis yang mengelilingi tepi objek nyata.

---

# 2. Struktur Topologi dan Konektivitas

Topologi menjawab pertanyaan:

- Berapa jumlah objek?
- Apakah objek memiliki hole?
- Apakah dua region saling terhubung?

Semua bergantung pada definisi konektivitas.

## 2.1 4-Connected dan 8-Connected

4-connected:

$$
N_4(p)=\{(x\pm1,y),(x,y\pm1)\}
$$

8-connected:

$$
N_8(p)=N_4(p)\cup\{(x\pm1,y\pm1)\}
$$

Perbedaan ini memengaruhi jumlah connected component ($C$) dan hole ($H$).

Euler characteristic:

$$
\chi = C - H
$$

Kesalahan konektivitas dapat mengubah interpretasi struktur objek dalam inspeksi industri.

---

## 2.2 Eksperimen — Pengaruh Konektivitas

Before: dua piksel diagonal  
After: jumlah komponen berbeda

```python
import cv2
import numpy as np

img = np.zeros((200,200), dtype=np.uint8)
img[80,80] = 255
img[81,81] = 255

num4,_ = cv2.connectedComponents(img, connectivity=4)
num8,_ = cv2.connectedComponents(img, connectivity=8)

print("Komponen 4-connected:", num4-1)
print("Komponen 8-connected:", num8-1)

img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
comparison = np.hstack((img_color, img_color))

cv2.imshow("Connectivity Analysis", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# 3. Representasi Parametrik Kontur

Kontur direpresentasikan sebagai:

$$
C = \{(x_1,y_1),(x_2,y_2),...,(x_N,y_N)\}
$$

Ini merupakan diskretisasi kurva kontinu:

$$
\gamma(t) = (x(t),y(t)), \quad t \in [0,1]
$$

Semakin besar $N$, semakin halus aproksimasi boundary.

---

## 3.1 Chain Approximation

### CHAIN_APPROX_NONE
- Semua titik boundary disimpan
- Presisi maksimum
- Memori $O(N)$

### CHAIN_APPROX_SIMPLE
- Titik kolinear dihapus
- Efisien untuk bentuk poligonal

---

## 3.2 Eksperimen — NONE vs SIMPLE

```python
import cv2
import numpy as np

img = np.zeros((400,400), dtype=np.uint8)
cv2.rectangle(img,(50,50),(350,350),255,-1)

contours_none,_ = cv2.findContours(
    img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

contours_simple,_ = cv2.findContours(
    img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("Titik NONE:", len(contours_none[0]))
print("Titik SIMPLE:", len(contours_simple[0]))

img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
comparison = np.hstack((img_color, img_color))

cv2.imshow("Chain Approximation", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Trade-off: presisi boundary vs efisiensi komputasi.

---

# 4. Properti Geometri Fundamental

---

## 4.1 Luas (Area)

$$
A=\frac12\left|\sum_{i=1}^N(x_i y_{i+1}-x_{i+1} y_i)\right|
$$

Merupakan bentuk diskret Green’s theorem.  
Kompleksitas: $O(N)$.

### Eksperimen — Area Before–After Noise

```python
import cv2
import numpy as np

clean = np.zeros((400,400,3), dtype=np.uint8)
cv2.circle(clean,(200,200),100,(255,255,255),-1)

noise = clean.copy()
cv2.circle(noise,(200,200),105,(255,255,255),2)

def compute_area(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,th = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    cnt,_ = cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnt)==0:
        return 0
    return cv2.contourArea(cnt[0])

print("Area Clean:",compute_area(clean))
print("Area Noise:",compute_area(noise))

comparison = np.hstack((clean, noise))
cv2.imshow("Area Stability", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Area relatif stabil terhadap noise kecil.

---

## 4.2 Perimeter

$$
P=\sum_{i=1}^N \sqrt{(x_{i+1}-x_i)^2+(y_{i+1}-y_i)^2}
$$

Sangat sensitif terhadap fluktuasi boundary.

Tambahkan pada eksperimen di atas:

```python
def compute_perimeter(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,th=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    cnt,_=cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnt)==0:
        return 0
    return cv2.arcLength(cnt[0],True)

print("Perimeter Clean:",compute_perimeter(clean))
print("Perimeter Noise:",compute_perimeter(noise))
```

Perimeter meningkat signifikan.

---

## 4.3 Circularity

$$
C=\frac{4\pi A}{P^2}
$$

Lingkaran ideal memiliki $C=1$.

### Eksperimen — Lingkaran vs Persegi

```python
import cv2
import numpy as np

img = np.zeros((400,800,3), dtype=np.uint8)
cv2.circle(img,(200,200),100,(255,255,255),-1)
cv2.rectangle(img,(450,100),(650,300),(255,255,255),-1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_,th = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

contours,_ = cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    A=cv2.contourArea(c)
    P=cv2.arcLength(c,True)
    if P==0:
        continue
    C=4*np.pi*A/(P**2)
    print("Circularity:",C)

comparison = np.hstack((img, img))
cv2.imshow("Circularity Comparison", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 4.4 Momen dan Centroid

$$
\bar{x} = \frac{M_{10}}{M_{00}}, \quad
\bar{y} = \frac{M_{01}}{M_{00}}
$$

Centroid adalah pusat distribusi massa.

### Eksperimen — Visualisasi Centroid

```python
import cv2
import numpy as np

img = np.zeros((400,400,3), dtype=np.uint8)
cv2.rectangle(img,(50,150),(200,300),(255,255,255),-1)

gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,th=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

contours,_=cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

output=img.copy()

for c in contours:
    M=cv2.moments(c)
    if M["m00"]==0:
        continue
    cx=int(M["m10"]/M["m00"])
    cy=int(M["m01"]/M["m00"])
    cv2.circle(output,(cx,cy),5,(0,0,255),-1)

comparison=np.hstack((img,output))
cv2.imshow("Centroid Visualization",comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# 5. Studi Kasus 1 — Inspeksi Lubang Baut

```python
import cv2
import numpy as np

img = cv2.imread("bolt.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

output = img.copy()

for cnt in contours:
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)

    if perimeter > 0:
        circularity = 4*np.pi*area/(perimeter**2)

        if circularity < 0.9:
            cv2.drawContours(output, [cnt], -1, (0,0,255), 3)
        else:
            cv2.drawContours(output, [cnt], -1, (0,255,0), 2)

comparison = np.hstack((img, output))

cv2.imshow("Bolt Circularity Inspection", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# 6. Studi Kasus 2 — Deteksi Retak Beton

```python
import cv2
import numpy as np

img = cv2.imread("crack.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 150)

kernel = np.ones((3,3), np.uint8)
morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(
    morph,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

output = img.copy()

for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)

    if min(w,h) > 0:
        aspect_ratio = max(w,h)/min(w,h)

        if aspect_ratio > 4:
            cv2.rectangle(output,(x,y),(x+w,y+h),(0,0,255),2)

comparison = np.hstack((img, output))

cv2.imshow("Concrete Crack Detection", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# 7. Studi Kasus 3 — Counting Objek pada Conveyor Industri

## Permasalahan

Pada sistem otomasi industri, diperlukan penghitungan jumlah produk yang lewat pada conveyor. Objek diasumsikan terpisah dan memiliki ukuran relatif seragam.

Parameter penting:

- Area minimum untuk menghindari noise
- Centroid untuk estimasi posisi

## Pipeline

Grayscale → Threshold → Morphology Open → Contour → Filter Area → Hitung Jumlah

```python
import cv2
import numpy as np

img = cv2.imread("conveyor.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

kernel = np.ones((5,5), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

contours, hierarchy = cv2.findContours(
    opening,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

output = img.copy()
count = 0

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 500:
        count += 1
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

cv2.putText(output, f"Count: {count}", (20,40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

comparison = np.hstack((img, output))

cv2.imshow("Object Counting", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Analisis Engineering:

- Kernel terlalu besar → objek kecil hilang
- Threshold salah → objek menyatu → undercount
- Overlapping objek → contour menyatu → perlu watershed

Kompleksitas tetap linear terhadap jumlah piksel.

---

# 8. Ringkasan Engineering

Contour analysis adalah transformasi dari domain piksel ke domain geometri.  
Area relatif stabil, perimeter sangat sensitif terhadap noise.  
Parameter threshold dan morfologi menentukan stabilitas topologi.  
Kesalahan awal memengaruhi sistem lanjutan seperti tracking, OCR, dan kontrol industri.

---

# 9. Mini Project Eksperimental

1. Analisis pengaruh resolusi terhadap perimeter  
2. Studi noise terhadap circularity  
3. Perbandingan CHAIN_APPROX_NONE vs SIMPLE  
4. Analisis deformasi objek  
5. Counting objek dengan overlapping  
6. Evaluasi kestabilan centroid pada noise  
7. Studi Euler number  
8. Integrasi contour ke SVM  
9. Analisis citra resolusi tinggi  
10. Tracking multi-objek berbasis contour  

---