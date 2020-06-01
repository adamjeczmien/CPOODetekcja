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




def init_player(cap):
    global frameSize, previousFrame, playButton, nextFrame, playFilm, framePerSec, changeFrame, maxFrames, windowName, windowName2, videoCap, nextFilm
    # button dimensions (y1,y2,x1,x2)
    #previous10Frames = [20, 60, 55, 95]
    previousFrame = [20,60,105,145]
    playButton = [20,60,155,245]
    nextFrame = [20,60,255,295]
    nextFilm = [20, 60, 305, 345]

    playFilm = 1
    changeFrame = 0
    windowName = 'Input'
    windowName2 = 'Output'

    videoCap = cap
    width = videoCap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = videoCap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frameSize = [int(height), int(width)]
    framePerSec = int(videoCap.get(cv2.CAP_PROP_FPS))
    maxFrames = int(videoCap.get(cv2.CAP_PROP_FRAME_COUNT))

    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, process_click)
    cv2.namedWindow(windowName2)
    cv2.setMouseCallback(windowName2, process_click)


def add_buttons_to_image(image):
    global frameSize, previousFrame, playButton, nextFrame, playFilm, framePerSec
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
    frame = int(videoCap.get(cv2.CAP_PROP_POS_FRAMES))

    textInfo = 'Frame:  '+str(frame)+'/' + str(maxFrames)
    cv2.putText(control_image, textInfo, (nextFilm[3]+20,nextFilm[0]+30), cv2.FONT_HERSHEY_PLAIN, 2, (180), 3)


    control_image = cv2.cvtColor(control_image, cv2.COLOR_GRAY2BGR)

    control_image[100:frameSize[0]+100, 0:frameSize[1]] = image
    return control_image



# function that handles the mousclicks
def process_click(event, x, y,flags, params):
    # check if the click is within the dimensions of the button
    global playFilm
    global changeFrame
    global videoCap
    global maxFrames
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > previousFrame[0] and y < previousFrame[1] and x > previousFrame[2] and x < previousFrame[3]:
            val = int(videoCap.get(cv2.CAP_PROP_POS_FRAMES))-2
            if val >= 0 & changeFrame == 0:
                playFilm = 0
                changeFrame = 1
                videoCap.set(cv2.CAP_PROP_POS_FRAMES, val)
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
                videoCap.set(cv2.CAP_PROP_POS_FRAMES, videoCap.get(cv2.CAP_PROP_FRAME_COUNT))
                playFilm = 1
                changeFrame = 1
                #videoCap.set(cv2.CAP_PROP_POS_FRAMES, val)
                #cv2.setTrackbarPos('Frame', windowName, val)



def run_player():
    global videoCap, windowName, windowName2, playFilm, changeFrame
    #data = []
    while videoCap.isOpened():
        if playFilm == 1:
            ret, frame = videoCap.read()
            if ret:
                framecopy = frame.copy()
                framecopy = filterFrame(framecopy)
                contoursToDraw = findSeabed(framecopy)

                final = frame.copy()
                findfish(framecopy, final, n_pix_enlarge=30)
                #df = createDataFrameFromContours(contoursToDraw.copy())
                cv2.drawContours(final, contoursToDraw, -1, (0, 255, 255), 2, offset=(0, 250))
                cv2.imshow(windowName, add_buttons_to_image(frame))
                cv2.imshow(windowName2, add_buttons_to_image(final))
            else:
                break
        else:
            if changeFrame == 1:
                ret, frame = videoCap.read()
                if ret:
                    framecopy = frame.copy()
                    framecopy = filterFrame(framecopy)
                    contoursToDraw = findSeabed(framecopy)

                    final = frame.copy()
                    findfish(framecopy, final, n_pix_enlarge=30)
                    #df = createDataFrameFromContours(contoursToDraw.copy())
                    cv2.drawContours(final, contoursToDraw, -1, (0, 255, 255), 2, offset=(0, 250))
                    cv2.imshow(windowName, add_buttons_to_image(frame))
                    cv2.imshow(windowName2, add_buttons_to_image(final))
                    changeFrame = 0
                else:
                    break
        cv2.waitKey(40)



def close_player():
    global videoCap
    videoCap.release()
    cv2.destroyWindow(windowName)
    cv2.destroyWindow(windowName2)



# create a window and attach a mousecallback and a trackbar

#windowPlayer(windowName, videoCap)
#ret, frame = videoCap.read()
#control_image = add_buttons_to_image(frame)

#show 'control panel'
