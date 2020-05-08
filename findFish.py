"""
    Rzeczy znalezc rybę potrzebuję.
    Odcienie szarości / maska na kolory ryby,
    Usuniecie Dna, patrzenie tylko powyzej dna

    Zaznaczenie ROI i narysowanie.

    potrzebne : - Usuniecie Menu
               - zaznacznie głębokości dna tak około (pomoże w zaznaczeniu do ilu pikseli skanować obraz)
"""
import numpy as np
import cv2


def findfish(frame, final):
    n = 5

    frame = frame[0:500, 0:1280]
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((11, 11), np.uint8)
    frame_gray = cv2.morphologyEx(frame_gray, cv2.MORPH_CLOSE, kernel)
    thresh, frame_gray = cv2.threshold(frame_gray, 60, 255, cv2.THRESH_BINARY)
    frame_gray = cv2.morphologyEx(frame_gray, cv2.MORPH_OPEN, kernel)
    frame_gray = cv2.morphologyEx(frame_gray, cv2.MORPH_CLOSE, kernel)

    # cv2.imshow('rybka_gray', frameGray)

    contours = cv2.findContours(frame_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    cnt = 0
    for c in contours:
        x1, y1, x2, y2 = cv2.boundingRect(c)

        # Żeby upewnić się, że kwadrat nie bedzie chcial dostac sie po przesunieciu poza obszar obrazka
        if x1 - n > 0:
            x_start = x1 - n
        else:
            x_start = 0

        if y1 - n > 0:
            y_start = y1 - n
        else:
            y_start = 0

        if x1 + x2 + n < frame.shape[1]:
            sum_x = x1 + x2 + n
        else:
            sum_x = frame.shape[1]

        if y1 + y2 + n < frame.shape[0]:
            sum_y = y1 + y2 + n
        else:
            sum_y = frame.shape[0]

        cv2.rectangle(final, (x_start, y_start), (sum_x, sum_y), (36, 255, 120), 2)
        cnt += 1

