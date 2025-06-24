import cv2

video = cv2.VideoCapture(0) # webcam

while True:
    ret, frame = video.read()
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not ret:
        break
    
    for y in range(frame.shape[0]): # altura
        for x in range(frame.shape[1]): # largura
            # if frame[y][x].mean() > 150:
            #     frame[y][x] = [255, 255, 255]
            # else:
            #     frame[y][x] = [0, 0, 0]
            if cinza[y][x] > 150:
                frame[y][x] = [255, 255, 255]
            else:
                frame[y][x] = [0, 0, 0]

    cv2.imshow("Webcam", frame)