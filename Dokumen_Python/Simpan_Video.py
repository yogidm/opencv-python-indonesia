import cv2

cap = cv2.VideoCapture(1)

# seting Codec yang akan digunakan yaitu XVID
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('keluaran.mp4',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # Gunakan baris dibawah ini jika dibutuhkan
        #frame = cv2.flip(frame,0)

        
        out.write(frame)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# matikan semua perangkat yang aktif
cap.release()
out.release()
cv2.destroyAllWindows()
