import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy


wCam , hCam = 800,800
frameR = 100 #Reduccion de frames 

detector = htm.handDetector(maxHands=1)

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

wScr, hScr = autopy.screen.size()


while True:
    success ,img = cap.read()
    img = detector.findHands(img)
    lmList,bbox = detector.findPosition(img)
    #print(lmList)
    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        #print(x1,y1,x2,y2)
    #  Cual dedo esta arriba?
    fingers = detector.fingersUp()
    print(fingers)


    #Dedo indice condicion
    cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),
    (255,0,255),2)
   
    if fingers[1]==1 and fingers[2]== 0:
     
    
    #Coordenadas pal mouse
        x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
        y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))

        #Mover el mouse
        #autopy.mouse.move(x3,y3)

        autopy.mouse.move(wScr- x3, y3)
        #SI SALGO DEL RECTANGULO SE CIERRA SOLO

        #circulo para marcar el dedo
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)

    #Dedos
    if fingers[0]==0 and fingers[1]==1 and fingers[2]== 1 and fingers[3]==0 and fingers[4]==0:
        length , img , lineInfo = detector.findDistance(8,12,img)
        #print(length)
        if length <20:
            cv2.circle(img,(lineInfo[4],lineInfo[5]),
            15,(0,255,0),cv2.FILLED)
            autopy.mouse.click()
           # autopy.key.Code(autopy.key.Code.LEFT_ARROW)
    if fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
        #length , img , lineInfo = detector.findDistance(8,12,img)
        autopy.mouse.click(autopy.mouse.Button.RIGHT)
    if fingers[0]==0 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
        autopy.key.tap(autopy.key.Code.LEFT_ARROW)
    if fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
        autopy.key.tap(autopy.key.Code.RIGHT_ARROW)
        #COMANDO POR DISTANCIA AGREGAR
    if fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
        autopy.key.tap(autopy.key.Code.F5)
    if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:
        autopy.key.tap(autopy.key.Code.ESCAPE)
    #if fingers[]
    
    cTime = time.time()
    
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    

    cv2.imshow('Imagen',img)  
    cv2.waitKey(1)  
