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
