import cv2
import numpy as np
from findFish import findfish
from filterFrame import *
from findSeabed import *
from dataAnalysisFuntions import *

videosNames = ['video_20190706_2019-07-06_174249', 'video_20190708_2019-07-08_182109', 'video_20190708_2019-07-08_182702',
              'video_20190708_2019-07-08_183022','video_20190708_2019-07-08_183118','video_20190708_2019-07-08_183217',
              'video_20190708_2019-07-08_183332','video_20190708_2019-07-08_185441','video_20190708_2019-07-08_185626',
              'video_20190708_2019-07-08_185932','video_20190712_2019-07-12_174940','video_20190712_2019-07-12_175210']

sourcePath = 'videos\\'




def init_player(film1, film2):
    global film_in, film_out, frameSize, previousFrame, playButton, nextFrame, playFilm, framePerSec, changeFrame, maxFrames, windowName, windowName2, videoCap, nextFilm, frameNumber
    # button dimensions (y1,y2,x1,x2)
    #previous10Frames = [20, 60, 55, 95]
    previousFrame = [20,60,5,45]
    playButton = [20,60,55,145]
    nextFrame = [20,60,155,195]
    nextFilm = [20, 60, 205, 245]

    playFilm = 1
    changeFrame = 0
    frameNumber= 0
    windowName = 'Input'
    windowName2 = 'Output'

    film_out = cv2.VideoCapture(film2)
    film_in = cv2.VideoCapture(film1)

    width = film_in.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = film_in.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frameSize = [int(height), int(width)]
    maxFrames = int(film_in.get(cv2.CAP_PROP_FRAME_COUNT))


    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, process_click)
    cv2.namedWindow(windowName2)
    cv2.setMouseCallback(windowName2, process_click)


def add_buttons_to_image(image):
    global frameSize, previousFrame, playButton, nextFrame, playFilm, framePerSec, frameNumber
    control_image = np.zeros((frameSize[0]+100,frameSize[1]), np.uint8)

    control_image[previousFrame[0]:previousFrame[1],previousFrame[2]:previousFrame[3]] = 180
    control_image[playButton[0]:playButton[1],playButton[2]:playButton[3]] = 180
    control_image[nextFrame[0]:nextFrame[1],nextFrame[2]:nextFrame[3]] = 180
    control_image[nextFilm[0]:nextFilm[1], nextFilm[2]:nextFilm[3]] = 180

    cv2.putText(control_image, '<',(previousFrame[2]+12,previousFrame[0]+30),cv2.FONT_HERSHEY_PLAIN, 2,(0),3)
    if playFilm == 0:
        cv2.putText(control_image, 'Play',(playButton[2]+12,playButton[0]+30),cv2.FONT_HERSHEY_PLAIN, 2,(0),3)
    else:
        cv2.putText(control_image, 'Stop', (playButton[2] + 12, playButton[0] + 30), cv2.FONT_HERSHEY_PLAIN, 2, (0), 3)
    cv2.putText(control_image, '>',(nextFrame[2]+12,nextFrame[0]+30),cv2.FONT_HERSHEY_PLAIN, 2,(0),3)
    cv2.putText(control_image, '>|', (nextFilm[2] + 8, nextFilm[0] + 30), cv2.FONT_HERSHEY_PLAIN, 2, (0), 3)

    #plot current frame

    textInfo = 'Frame:  '+str(int(film_in.get(cv2.CAP_PROP_POS_FRAMES)))+'/' + str(maxFrames)
    cv2.putText(control_image, textInfo, (nextFilm[3]+20,nextFilm[0]+30), cv2.FONT_HERSHEY_PLAIN, 2, (180), 3)


    control_image = cv2.cvtColor(control_image, cv2.COLOR_GRAY2BGR)

    control_image[100:frameSize[0]+100, 0:frameSize[1]] = image
    return control_image



# function that handles the mousclicks
def process_click(event, x, y,flags, params):
    # check if the click is within the dimensions of the button
    global playFilm
    global changeFrame
    global maxFrames, frameNumber
    global previousFrame, playButton, nextFrame, nextFilm

    if event == cv2.EVENT_LBUTTONDOWN:
        if y > previousFrame[0] and y < previousFrame[1] and x > previousFrame[2] and x < previousFrame[3]:
            val = film_in.get(cv2.CAP_PROP_POS_FRAMES)-2
            if val >= 0 & changeFrame == 0:
                film_in.set(cv2.CAP_PROP_POS_FRAMES, val)
                film_out.set(cv2.CAP_PROP_POS_FRAMES, val)
                playFilm = 0
                changeFrame = 1
                frameNumber = val
                #cv2.setTrackbarPos('Frame', windowName, val)
        if y > playButton[0] and y < playButton[1] and x > playButton[2] and x < playButton[3]:
            changeFrame = 0
            if playFilm:
                playFilm = 0
                changeFrame = 1
                #print('Stop film!')
            else:
                playFilm = 1
                #print('Run film!')
        if y > nextFrame[0] and y < nextFrame[1] and x > nextFrame[2] and x < nextFrame[3]:
            if changeFrame == 0:
                playFilm = 0
                changeFrame = 1
        if y > nextFilm[0] and y < nextFilm[1] and x > nextFilm[2] and x < nextFilm[3]:
            if changeFrame == 0:
                film_in.set(cv2.CAP_PROP_POS_FRAMES, maxFrames)
                film_out.set(cv2.CAP_PROP_POS_FRAMES, maxFrames)
                playFilm = 1
                changeFrame = 1
                #videoCap.set(cv2.CAP_PROP_POS_FRAMES, val)
                #cv2.setTrackbarPos('Frame', windowName, val)



def run_player():
    global videoCap, windowName, windowName2, playFilm, changeFrame, frameNumber, maxFrames, film_in, film_out
    #data = []
    while film_in.isOpened() & film_out.isOpened():
        if playFilm == 1:
            ret_in, frame_in = film_in.read()
            ret_out, frame_out = film_out.read()
            if ret_out & ret_in:
                cv2.imshow(windowName, add_buttons_to_image(frame_in))
                cv2.imshow(windowName2, add_buttons_to_image(frame_out))
            else:
                break
        else:
            if changeFrame == 1:
                ret_in, frame_in = film_in.read()
                ret_out, frame_out = film_out.read()
                if ret_out & ret_in:
                    cv2.imshow(windowName, add_buttons_to_image(frame_in))
                    cv2.imshow(windowName2, add_buttons_to_image(frame_out))
                    changeFrame = 0
                else:
                    break
        cv2.waitKey(40)



def close_player():
    global film_in, film_out
    film_in.release()
    film_out.release()
    cv2.destroyWindow(windowName)
    cv2.destroyWindow(windowName2)



# create a window and attach a mousecallback and a trackbar

#windowPlayer(windowName, videoCap)
#ret, frame = videoCap.read()
#control_image = add_buttons_to_image(frame)

#show 'control panel'
