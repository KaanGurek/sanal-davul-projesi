import cv2
import numpy as np
import pygame

pygame.mixer.init() 
try:
    s1 = pygame.mixer.Sound("kick.mp3")
    s2 = pygame.mixer.Sound("snare.mp3")
    s3 = pygame.mixer.Sound("hihat.mp3")
except:
    print("Müzik dosyaları bulunamadı! İsimleri kontrol et.")

# 2. Mavi Nesne HSV Aralıkları
lower_blue = np.array([100, 150, 50]) 
upper_blue = np.array([140, 255, 255])

cap = cv2.VideoCapture(0) 


drums = [ 
    [40, 100, 190, 250, s1, False, "KICK"],   
    [245, 50, 395, 200, s2, False, "SNARE"],  
    [450, 100, 600, 250, s3, False, "HI-HAT"] 
]

while True:                       
    ret, frame = cap.read()
    if not ret: break
    
    frame = cv2.flip(frame, 1)   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)           
    
    # 3. Renk Maskeleme ve Filtreleme
    mask = cv2.inRange(hsv, lower_blue, upper_blue)  
    mask = cv2.medianBlur(mask, 7)  
    
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
    center = None 
    if len(cnts) > 0:  
        c = max(cnts, key=cv2.contourArea) 
        if cv2.contourArea(c) > 600: 
            M = cv2.moments(c) 
            if M["m00"] > 0: 
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 
                cv2.circle(frame, center, 10, (255, 255, 255), -1) 

    
    for d in drums: 
        
        x1, y1, x2, y2, sound, is_active, name = d 
        
        if center and x1 < center[0] < x2 and y1 < center[1] < y2: 
            if not d[5]:  
                sound.play()
                d[5] = True 
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3) 
        else:
            d[5] = False  
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    
        cv2.putText(frame, name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Davul Simulator", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release() 
cv2.destroyAllWindows()