"""
A więc aby znalezc rybę patrzymy na cały Frame
Chcemy jednak aby nie zaznaczało nam Dna jako ROI.
Aby tak było wyznaczamy Obwiednie Czarnych obszarów we Frame'ie.
Następnie zawsze wybieramy najwiekszy(przy założeniu, że dno jest niżej a nie wyżej -> nie nadaje się na płytkie wody).
Gdy mamy największy Fillujemy go kolorem Białym.
Następnie posiadając maskę, która czarna jest dla dna i poniżej możemy BITWISE_AND co pozwoli na wyciecie Dna z obszaru,
w którym może pojawić się ROI.

"""
import numpy as np
import cv2


def findfish(frame, final, n_pix_enlarge=0):
    frame = frame[0:720, 0:1280]
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((11, 11), np.uint8)
    frame_gray = cv2.morphologyEx(frame_gray, cv2.MORPH_CLOSE, kernel)
    thresh, frame_gray = cv2.threshold(frame_gray, 50, 255, cv2.THRESH_BINARY)
    thresh_inv, frame_gray_inv = cv2.threshold(frame_gray, 0, 120, cv2.THRESH_BINARY_INV)

    frame_gray = cv2.morphologyEx(frame_gray, cv2.MORPH_OPEN, kernel)
    frame_gray = cv2.morphologyEx(frame_gray, cv2.MORPH_CLOSE, kernel)

    frame_gray_inv = cv2.morphologyEx(frame_gray_inv, cv2.MORPH_OPEN, kernel)
    frame_gray_inv = cv2.morphologyEx(frame_gray_inv, cv2.MORPH_CLOSE, kernel)

    # Odcinanie Dna
    contours, hierarchy = cv2.findContours(frame_gray_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # bierzemy pod uwagę tylko największą obwiednie
    # ( problematyczne będzie to gdy ta obwiednia będzie nie na górze a na dole no ale cóż)
    contour_max = 0
    perimeter_max = 0
    for cidx, contour in enumerate(contours):
        if cv2.arcLength(contour, True) > perimeter_max:
            contour_max = contour
            perimeter_max = cv2.arcLength(contour, True)

    # Odcinanie cyfr i łódki - Hardcode
    pts_numbers = np.array([[0, 0], [1279, 0], [535, 60], [0, 375]], np.int32).reshape((-1, 1, 2))
    pts_boat = np.array([[1120, 15], [1250, 15], [1250, 150], [1120, 150]], np.int32).reshape((-1, 1, 2))

    # Konstrukcja Maski - czarne nie jest brane pod uwagę
    mask = np.zeros([720, 1280], np.uint8)
    # Contours MAX określa region, który chcemy widzieć więc na biało
    cv2.drawContours(mask, [contour_max], -1, 255, -1)
    # Boat i Numbers na czarno ponieważ to nie są obszary, w których chcemy szukać
    cv2.drawContours(mask, [pts_numbers,  pts_boat], -1, 0, -1)
    #cv2.imshow('rybka_gray', mask)

    # Nałożenie maski
    frame_gray = cv2.bitwise_and(mask, frame_gray)
    #cv2.imshow('frame_gray', frame_gray)

    # FISHY FINDERS
    contours = cv2.findContours(frame_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Rysowanie Prostokątów ROI
    cnt = 0
    for c in contours:
        x1, y1, x2, y2 = cv2.boundingRect(c)

        # powiększanie o N tak aby nie wychodził on poza image
        # Żeby upewnić się, że kwadrat nie bedzie chcial dostac sie po przesunieciu poza obszar obrazka
        if x1 - n_pix_enlarge > 0:
            x_start = x1 - n_pix_enlarge
        else:
            x_start = 0

        if y1 - n_pix_enlarge > 0:
            y_start = y1 - n_pix_enlarge
        else:
            y_start = 0

        if x1 + x2 + n_pix_enlarge < frame.shape[1]:
            sum_x = x1 + x2 + n_pix_enlarge
        else:
            sum_x = frame.shape[1]

        if y1 + y2 + n_pix_enlarge < frame.shape[0]:
            sum_y = y1 + y2 + n_pix_enlarge
        else:
            sum_y = frame.shape[0]

        cv2.rectangle(final, (x_start, y_start), (sum_x, sum_y), (36, 255, 120), 2)
        cv2.putText(final, f"Fishie_{cnt}", (sum_x-20, y_start-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 120))
        cnt += 1
