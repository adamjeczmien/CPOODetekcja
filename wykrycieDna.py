"""READ ME

Skrypt działa, przy założeniu, że pliki video znajdują się w folderze o nazwie 'video'. Foler ten powinien być zlokalizowany
w tym samym miejscu co projekt. Jeśli lokalizacja plików video jest inna zmień obiekt 'sourcePath'.

Zamknięcie aktualnego filmu i przejście do następnego -> wciśnij klawisz 'q'

Sposób działania:

 - Zamiana koloru na odcienie szarości
 - Zamknięcie morfologiczne
 - Progowanie
 - Otwarcie + zamknięcie
 - Znalezienie krawędzi - filtr cannyego
 - Wykluczenie konturów krótszych niż X
 - Prezentacja

TODO Usunięcie menu
todo Obcięcie części obrazka (wstępnie od 2,5m do Dużego menu)
todo Usunięcie małych menu (przyciski na obrazie wpływają na wynik)
todo Wyciągnięcie współrzędnych konturów (Może się przydać do obrazowania głębokości)
"""

import cv2
import numpy as np

videonames = ['video_20190706_2019-07-06_174249','video_20190708_2019-07-08_182109','video_20190708_2019-07-08_182702',
              'video_20190708_2019-07-08_183022','video_20190708_2019-07-08_183118','video_20190708_2019-07-08_183217',
              'video_20190708_2019-07-08_183332','video_20190708_2019-07-08_185441','video_20190708_2019-07-08_185626',
              'video_20190708_2019-07-08_185932','video_20190712_2019-07-12_174940','video_20190712_2019-07-12_175210']



sourcePath = 'videos\\'

for name in videonames:

    cap = cv2.VideoCapture(sourcePath + name +'.mp4')

    if (cap.isOpened()== False):
      print("Error opening video file"+sourcePath + name +'.mp4')

    kernel = np.ones((10,10),np.uint8)

    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True:
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frameGray = cv2.morphologyEx(frameGray, cv2.MORPH_CLOSE, kernel)
            thresh, frameGray= cv2.threshold(frameGray,50,255,cv2.THRESH_BINARY_INV)
            frameGray = cv2.morphologyEx(frameGray, cv2.MORPH_OPEN,kernel)
            frameGray = cv2.morphologyEx(frameGray, cv2.MORPH_CLOSE, kernel)
            edges = cv2.Canny(frameGray, 50, 50)
            contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            contoursToDraw = contours.copy()
            contoursToDraw.clear()
            for i in range(len(contours)):
                if cv2.arcLength(contours[i],False)>800:
                    contoursToDraw.append(contours[i])

            edgesColors = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            final = frame.copy()
            cv2.drawContours(final,contoursToDraw,-1,(0,255,255),2)
            cv2.imshow('Input', frame)
            cv2.imshow('Final', final)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    # When everything done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

