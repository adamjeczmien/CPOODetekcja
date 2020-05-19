import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


def assignZAxis(listOfDataFrames): # Wersja robocza - docelowo powinno przypisywac jakas wartosc w metrach
    z = np.linspace(0, len(listOfDataFrames) - 1, len(listOfDataFrames))
    for i in z:
        listOfDataFrames[int(i)]["Z"] = int(i)
    return listOfDataFrames


def createPointCloud(listOfDataFrames):
    inputDF = listOfDataFrames
    DataFrames = assignZAxis(inputDF)
    dataFinal = DataFrames[0]
    z = np.linspace(0, len(DataFrames) - 1, len(DataFrames))
    for i in z:
        dataFinal = dataFinal.append(DataFrames[int(i)])
    dataFinal = dataFinal.reset_index()
    return dataFinal


def createDataFrameFromContours(contours):
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
    df.columns = ['X', 'Y']
    return df


def make3DPlotForDataFrame(dataFrame):
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(-(dataFrame['X']), dataFrame['Z'], -(250 + dataFrame['Y']), cmap='viridis')
    ax.set_xlabel('pixels')
    ax.set_ylabel('Frame No.')
    ax.set_zlabel('pixels')
    axes = plt.gca()
    axes.set_zlim([-720, 0])
    fig = plt.gcf()
    fig.set_size_inches(11, 8)
    plt.show()


def pixelsIntoMeters():
    # TO DO
    print(0)

