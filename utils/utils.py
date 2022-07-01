import random
import time
import d3dshot
import cv2
import numpy as np
from PIL import Image
import pyautogui
import xxhash

d3 = d3dshot.create(capture_output='numpy')


def cacheObjectPos(func):
    lastX = None
    lastY = None
    lastW = None
    lastH = None
    lastImgHash = None

    def inner(screenshot):
        nonlocal lastX, lastY, lastW, lastH, lastImgHash
        if(lastX != None and lastY != None and lastW != None and lastH != None):
            copiedImg = np.ascontiguousarray(screenshot[lastY:lastY +
                                                        lastH, lastX:lastX + lastW])
            copiedImgHash = hashit(copiedImg)
            if copiedImgHash == lastImgHash:
                return (lastX, lastY, lastW, lastH)
        res = func(screenshot)
        didntMatch = res is None
        if didntMatch:
            return None
        (x, y, w, h) = res
        lastX = x
        lastY = y
        lastW = w
        lastH = h
        lastImg = np.ascontiguousarray(
            screenshot[lastY:lastY + lastH, lastX:lastX + lastW])
        lastImgHash = hashit(lastImg)
        return (x, y, w, h)
    return inner


def getAdjacencyMatrix(arr):
    repArrHorizontal = np.ravel(arr)
    arrDim = arr.shape[0] * arr.shape[1]
    arrShape = (arrDim, arrDim)
    repArr = np.broadcast_to(repArrHorizontal, arrShape)
    seqArr = np.arange(1, arrDim + 1)
    verticesWithPossibleRightConnections = np.eye(arrDim, k=1)
    indexesWithPossibleRightConnections = np.where(seqArr % arr.shape[1] == 0, 0, 1)
    indexesWithPossibleRightConnections = np.broadcast_to(indexesWithPossibleRightConnections, arrShape)
    indexesWithPossibleRightConnections = np.rot90(indexesWithPossibleRightConnections, k=-1)
    rightConnections = np.multiply(verticesWithPossibleRightConnections, indexesWithPossibleRightConnections)
    verticesWithPossibleLeftConnections = np.eye(arrDim, k=-1)
    indexesWithPossibleLeftConnections = np.flip(indexesWithPossibleRightConnections)
    leftConnections = np.multiply(verticesWithPossibleLeftConnections, indexesWithPossibleLeftConnections)
    topConnections = np.eye(arrDim, k=-arr.shape[1])
    bottomConnections = np.eye(arrDim, k=arr.shape[1])
    topBottomConnections = np.add(topConnections, bottomConnections)
    leftRightConnections = np.add(leftConnections, rightConnections)
    connections = np.add(topBottomConnections, leftRightConnections)
    connections = np.multiply(connections, repArr)
    connections = np.multiply(connections, np.rot90(repArr, k=-1))
    return connections


def getCenterOfBounds(bounds):
    (left, top, width, height) = bounds
    center = (left + width / 2, top + height / 2)
    return center


def getCoordinateFromPixel(pixel):
    x, y = pixel
    return (x + 31744, y + 30976)


def getPixelFromCoordinate(coordinate):
    x, y, _ = coordinate
    return (x - 31744, y - 30976)


def getSquareMeterSize():
    return 51.455


def graysToBlack(arr):
    return np.where(np.logical_and(arr >= 50, arr <= 100), 0, arr)


def hashit(arr):
    return xxhash.xxh64(np.ascontiguousarray(arr), seed=20220605).intdigest()


def hashitHex(arr):
    return xxhash.xxh64(np.ascontiguousarray(arr), seed=20220605).hexdigest()


def hasMatrixInsideOther(matrix, other):
    matrixFlattened = matrix.flatten()
    otherFlattened = other.flatten()
    blackPixelsIndexes = np.nonzero(otherFlattened == 0)[0]
    blackPixels = np.take(matrixFlattened, blackPixelsIndexes)
    didMatch = np.all(blackPixels == 0)
    return True if didMatch else False


def loadImg(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)


def loadImgAsArray(path):
    return np.array(loadImg(path))


def locate(compareImg, img, confidence=0.85):
    match = cv2.matchTemplate(compareImg, img, cv2.TM_CCOEFF_NORMED)
    res = cv2.minMaxLoc(match)
    matchConfidence = res[1]
    didntMatch = matchConfidence <= confidence
    if didntMatch:
        return None
    (x, y) = res[3]
    width = len(img[0])
    height = len(img)
    return (x, y, width, height)


def getScreenshot(window):
    region = (window.top, window.left, window.width - 15, window.height)
    screenshot = d3.screenshot(region=region)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    return screenshot


def press(key):
    pyautogui.press(key)


def typeKeyboard(phrase):

    words = list(phrase)
    for word in words:
        time.sleep(random.randrange(70, 190)/1000)
        press(word)
    time.sleep(random.randrange(70, 190) / 1000)
    press('enter')


def rightClick(x, y):
    pyautogui.rightClick(x, y)


def saveImg(arr, name):
    im = Image.fromarray(arr)
    im.save(name)

def cropImg(img, x, y, width, height):
    return img[y:y+height, x:x+width]

def randomCoord(x,y,width,height):
    x = random.randrange(x, x+width)
    y = random.randrange(y, y+height)

    return (x,y)