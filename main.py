"""READ ME

Skrypt działa, przy założeniu, że pliki video znajdują się w folderze o nazwie 'video'. Foler ten powinien być zlokalizowany
w tym samym miejscu co projekt. Jeśli lokalizacja plików video jest inna zmień obiekt 'sourcePath'.

Zamknięcie aktualnego filmu i przejście do następnego -> wciśnij klawisz 'q'
"""

from filterFrame import *
from findSeabed import *
import cv2
videonames = ['video_20190706_2019-07-06_174249','video_20190708_2019-07-08_182109','video_20190708_2019-07-08_182702',
              'video_20190708_2019-07-08_183022','video_20190708_2019-07-08_183118','video_20190708_2019-07-08_183217',
              'video_20190708_2019-07-08_183332','video_20190708_2019-07-08_185441','video_20190708_2019-07-08_185626',
              'video_20190708_2019-07-08_185932','video_20190712_2019-07-12_174940','video_20190712_2019-07-12_175210']

sourcePath = 'videos\\'

for name in videonames:

    cap = cv2.VideoCapture(sourcePath + name +'.mp4')

    if (cap.isOpened()== False):
      print("Error opening video file"+sourcePath + name +'.mp4')

    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True:
            framecopy = frame.copy()
            framecopy = filterFrame(framecopy)
            contoursToDraw = findSeabed(framecopy)
            final = frame.copy()
            cv2.drawContours(final,contoursToDraw,-1,(0,255,255),2,offset=(0,250))
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
