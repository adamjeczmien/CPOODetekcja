import cv2
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split

# data preparation
# dimensions match the size of images extracted from video
dim = (70, 70)
sourcePath = 'numbers_train\\'
digitsList = []

for name in range(10):
    digit = cv2.imread(sourcePath + str(name) + '.jpg')
    digit = cv2.cvtColor(digit, cv2.COLOR_BGR2GRAY)
    digit = cv2.threshold(digit, 100, 255, cv2.THRESH_BINARY)[1]
    digit = cv2.resize(digit, dim)
    digitsList.append(digit)

# images added again as a test set
for name in range(10):
    digit = cv2.imread(sourcePath + str(name) + '.jpg')
    digit = cv2.cvtColor(digit, cv2.COLOR_BGR2GRAY)
    digit = cv2.threshold(digit, 100, 255, cv2.THRESH_BINARY)[1]
    digit = cv2.resize(digit, dim)
    digitsList.append(digit)

digits = np.array(digitsList)
target = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# model learning
n_samples = len(digits)
data = digits.reshape((n_samples, -1))
classifier = svm.SVC()
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.5, shuffle=False)

classifier.fit(X_train, y_train)


def findNumber(image):
    image = prepareImage(image)
    n = classifier.predict(image)
    return n


def prepareImage(image):
    image = cv2.bitwise_not(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
    image = image.reshape((1, -1))
    return image
