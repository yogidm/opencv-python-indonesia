import cv2 # Masukkan pustaka OpenCV

# Membaca file video dan masukkan pada variabel
cap = cv2.VideoCapture(0)

while(cap.isOpened()): # lakukan pembacaan pada semua frame
    ret, frame = cap.read() #frame siap untuk diolah

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Tampilkan frame
    cv2.imshow('Frame Ori',frame)
    cv2.imshow('Frame Gray',gray)

    # Tahan frame selama 1ms
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
# Lepas capture dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
