"""READ ME

Skrypt działa, przy założeniu, że pliki video znajdują się w folderze o nazwie 'video'. Folder ten powinien
być zlokalizowany w tym samym miejscu co projekt. Jeśli lokalizacja plików video jest inna zmień obiekt 'sourcePath'.

Zamknięcie aktualnego filmu i przejście do następnego -> wciśnij klawisz 'q'
"""
from findFish import findfish
from filterFrame import *
from findSeabed import *
from dataAnalysisFuntions import *
from interface import *
import cv2

# UWAGA!
# Mozna sobie obejrzec wykres dna dla kolejnych wideo ale nie daje gwarancji, ze program sie dokonczy wykonywac
# Bo niektore chmury potrzebuja zbyt duzej ilosci pamieci
showPlot = False


videosNames = ['video_20190706_2019-07-06_174249', 'video_20190708_2019-07-08_182109', 'video_20190708_2019-07-08_182702',
              'video_20190708_2019-07-08_183022','video_20190708_2019-07-08_183118','video_20190708_2019-07-08_183217',
              'video_20190708_2019-07-08_183332','video_20190708_2019-07-08_185441','video_20190708_2019-07-08_185626',
              'video_20190708_2019-07-08_185932','video_20190712_2019-07-12_174940','video_20190712_2019-07-12_175210']

sourcePath = 'videos\\'
cloud = []
for name in videosNames:
    cap = cv2.VideoCapture(sourcePath + name + '.mp4')


    cap = cv2.VideoCapture(sourcePath + name + '.mp4')

    if not cap.isOpened():
        print("Error opening video file"+sourcePath + name + '.mp4')

    framecnt = 0
    # list of dataframes used to generate point cloud
    data = []



    out_path = "videos_out\\" + name + "_out.mp4"
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out_film2 = cv2.VideoWriter(out_path,cv2.VideoWriter_fourcc('M','P','4','V'), cap.get(cv2.CAP_PROP_FPS), size)

    print('Beginning of the calculation of the seabed')
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            framecnt += 1
            framecopy = frame.copy()
            framecopy = filterFrame(framecopy)
            contoursToDraw = findSeabed(framecopy)

            final = frame.copy()
            findfish(framecopy, final, n_pix_enlarge=30)

            centerDepth = getDepthInMeters(final)
            df = createDataFrameFromContours(contoursToDraw.copy(), centerDepth)
            data.append(df)
            cv2.drawContours(final, contoursToDraw, -1, (0, 255, 255), 2, offset=(0, 250))

            out_film2.write(final)
            cv2.imshow('Final', final)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    print('Saving output video to' + out_path)
    out_film2.release()

    init_player(sourcePath + name + '.mp4', out_path)
    run_player()

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()
    print("Done with: "+ name + ".mp4")
    print("Frames of the video: " + str(framecnt))
    print("Calculating cloud for: " + name + ".mp4")
    dataFinal = createPointCloud(data)
    if showPlot:
        print("Creating 3D plot for: " + name + ".mp4")
        make3DPlotForDataFrame(dataFinal)
    cloud.append(dataFinal)
    print("Video :" + name + " finished")


for i in range(len(cloud)):
    print("Data Points cloud for: " + videosNames[int(i) - 1] + ".mp4")
    print(cloud[int(i)-1])

