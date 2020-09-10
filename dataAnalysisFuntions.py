import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

from numberRecognition import findNumber


def createPointCloud(listOfDataFrames):
    inputDF = listOfDataFrames
    DataFrames = assignYAxis(inputDF)
    dataFinal = DataFrames[0]
    z = np.linspace(0, len(DataFrames) - 1, len(DataFrames))
    for i in z:
        dataFinal = dataFinal.append(DataFrames[int(i)])
    dataFinal = dataFinal.reset_index()
    return dataFinal


def assignYAxis(listOfDataFrames):
    # assign Y axis value according to frame number
    z = np.linspace(0, len(listOfDataFrames) - 1, len(listOfDataFrames))
    for i in z:
        listOfDataFrames[int(i)]["Y"] = int(i)
    return listOfDataFrames


def createDataFrameFromContours(contours, centerDepth):
    contoursCopy = contours.copy()
    if len(contours) == 2:
        # choose contour closer to surface
        meany1 = np.mean(contoursCopy[0][0, 0, 1])
        meany2 = np.mean(contoursCopy[1][0, 0, 1])
        if meany1 > meany2:
            chosenContour = 1
        else:
            chosenContour = 0
    else:
        chosenContour = 0
    oneContour = contoursCopy[chosenContour][:, 0, :]
    df = pd.DataFrame(oneContour)
    df.astype(float)
    df.columns = ['X', 'Z']
    assignZAxis(df, centerDepth)
    return df


def assignZAxis(dataFrame, centerDepth):
    # calculation using pixel value of depth in center point, where depth is measured
    centerPixels = 250 + dataFrame['Z'][529]
    zValue = (250 + dataFrame['Z'])
    zValue = pixelsIntoMeters(zValue, centerDepth, centerPixels)
    dataFrame['Z'] = zValue


def pixelsIntoMeters(zValue, centerDepth, centerPixels):
    mPerPixel = centerDepth/centerPixels
    return mPerPixel*zValue


def getDepthInMeters(videoFrame):
    numberFirst = videoFrame[20:90, 50:120]
    numberSecond = videoFrame[20:90, 120:190]

    depth = findNumber(numberFirst) + (findNumber(numberSecond) * 0.1)
    return depth


def make3DPlotForDataFrame(dataFrame):
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(-(dataFrame['X']), dataFrame['Y'], -(dataFrame['Z']), cmap='viridis')
    ax.set_xlabel('pixels')
    ax.set_ylabel('Frame No.')
    ax.set_zlabel('depth [m]')
    maxDepth = (dataFrame['Z'].max() + 1).round()
    axes = plt.gca()
    axes.set_zlim([-maxDepth, 0])
    fig = plt.gcf()
    fig.set_size_inches(11, 8)
    plt.show()