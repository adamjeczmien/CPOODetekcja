"""READ ME

Sposób działania:
 - Obcięcie części obrazka (od 2,5m do Dużego menu)
 - Zamiana koloru na odcienie szarości
 - Zamknięcie morfologiczne
 - Progowanie
 - Otwarcie + zamknięcie
 - Znalezienie krawędzi - filtr cannyego
 - Wykluczenie konturów krótszych niż X
 - Prezentacja
 - Zwracanie wszystkich punktów, ktore naleza do konturu dna

TODO
todo Usunięcie małych menu (przyciski na obrazie wpływają na wynik)
"""

import cv2
import numpy as np

def findSeabed(frame):
    frame = frame[0:720, 0:1280]
    #From 2,5m to bottom menu
    frame = frame[250:720, 0:1280]
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((10, 10), np.uint8)
    frameGray = cv2.morphologyEx(frameGray, cv2.MORPH_CLOSE, kernel)
    thresh, frameGray = cv2.threshold(frameGray, 50, 255, cv2.THRESH_BINARY_INV)
    frameGray = cv2.morphologyEx(frameGray, cv2.MORPH_OPEN, kernel)
    frameGray = cv2.morphologyEx(frameGray, cv2.MORPH_CLOSE, kernel)
    edges = cv2.Canny(frameGray, 50, 50)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # zwracaj wszystkie punkty
    contoursToDraw = contours.copy()
    contoursToDraw.clear()
    for i in range(len(contours)):
        if cv2.arcLength(contours[i], False) > 800:
            contoursToDraw.append(contours[i])

    return contoursToDraw

