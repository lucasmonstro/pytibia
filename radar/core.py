import numpy as np
import pyautogui
from radar import config, types
import utils.core
from scipy.spatial import distance
from time import sleep


def getCoordinate(screenshot, previousCoordinate=None):
    floorLevel = getFloorLevel(screenshot)
    cannotGetFloorLevel = floorLevel is None
    if cannotGetFloorLevel:
        return None
    radarToolsPos = getRadarToolsPos(screenshot)
    cannotGetRadarToolsPos = radarToolsPos is None
    if cannotGetRadarToolsPos:
        return None
    radarImg = getRadarImg(screenshot, radarToolsPos)
    radarHashedImg = utils.core.hashitHex(radarImg)
    shouldGetCoordinateByCachedRadarHashedImg = radarHashedImg in config.coordinates
    if shouldGetCoordinateByCachedRadarHashedImg:
        return config.coordinates[radarHashedImg]
    shouldGetCoordinateByPreviousCoordinateArea = previousCoordinate is not None
    if shouldGetCoordinateByPreviousCoordinateArea:
        (previousCoordinateXPixel, previousCoordinateYPixel) = utils.core.getPixelFromCoordinate(previousCoordinate)
        paddingSize = 20
        yStart = previousCoordinateYPixel - (config.dimensions["halfHeight"] + paddingSize)
        yEnd = previousCoordinateYPixel + (config.dimensions["halfHeight"] + 1 + paddingSize)
        xStart = previousCoordinateXPixel - (config.dimensions["halfWidth"] + paddingSize)
        xEnd = previousCoordinateXPixel + (config.dimensions["halfWidth"] + paddingSize)
        areaImgToCompare = config.floorsImgs[floorLevel][yStart:yEnd, xStart:xEnd]
        areaFoundImg = utils.core.locate(
            areaImgToCompare, radarImg, confidence=0.9)
        if areaFoundImg:
            currentCoordinateXPixel = previousCoordinateXPixel - paddingSize + areaFoundImg[0]
            currentCoordinateYPixel = previousCoordinateYPixel - paddingSize + areaFoundImg[1]
            (currentCoordinateX, currentCoordinateY) = utils.core.getCoordinateFromPixel((currentCoordinateXPixel, currentCoordinateYPixel))
            return (currentCoordinateX, currentCoordinateY, floorLevel)
    # config.floorsConfidence[floorLevel]
    imgCoordinate = utils.core.locate(
        config.floorsImgs[floorLevel], radarImg, confidence=0.75)
    cannotGetImgCoordinate = imgCoordinate is None
    if cannotGetImgCoordinate:
        return None
    xImgCoordinate = imgCoordinate[0] + config.dimensions["halfWidth"]
    yImgCoordinate = imgCoordinate[1] + config.dimensions["halfHeight"]
    xCoordinate, yCoordinate = utils.core.getCoordinateFromPixel((xImgCoordinate, yImgCoordinate))
    return (xCoordinate, yCoordinate, floorLevel)


def getFloorLevel(screenshot):
    radarToolsPos = getRadarToolsPos(screenshot)
    radarToolsPosIsEmpty = radarToolsPos is None
    if radarToolsPosIsEmpty:
        return None
    left, top, width, height = radarToolsPos
    left = left + width + 8
    top = top - 7
    height = 67
    width = 2
    floorLevelImg = screenshot[top:top + height, left:left + width]
    floorImgHash = utils.core.hashit(floorLevelImg)
    hashNotExists = not floorImgHash in config.floorsLevelsImgsHashes
    if hashNotExists:
        return None
    floorLevel = config.floorsLevelsImgsHashes[floorImgHash]
    return floorLevel


def getRadarImg(screenshot, radarToolsPos):
    radarToolsPosX = radarToolsPos[0]
    radarToolsPosY = radarToolsPos[1]
    x0 = radarToolsPosX - config.dimensions['width'] - 11
    x1 = x0 + config.dimensions['width']
    y0 = radarToolsPosY - 50
    y1 = y0 + config.dimensions['height']
    radarImage = screenshot[y0:y1, x0:x1]
    return radarImage


@utils.core.cacheObjectPos
def getRadarToolsPos(screenshot):
    return utils.core.locate(screenshot, config.images['tools'])


def getWaypointIndexFromClosestCoordinate(coordinate, waypoints):
    (_, _, floorLevel) = coordinate
    waypointsIndexes = np.nonzero(waypoints['coordinate'][:, 2] == floorLevel)[0]
    hasNoWaypointsIndexes = len(waypointsIndexes) == 0
    if hasNoWaypointsIndexes:
        return
    possibleWaypoints = np.array([(waypointIndex, distance.euclidean(waypoints[waypointIndex]['coordinate'], coordinate))
                                for waypointIndex in waypointsIndexes], dtype=types.waypointDistanceType)
    sortedWaypoints = np.sort(possibleWaypoints, order='distance')
    return sortedWaypoints[0]['index']


def goToCoordinate(screenshot, playerCoordinate, coordinate):
    (radarToolsPosX, radarToolsPosY, _, _) = getRadarToolsPos(screenshot)
    x0 = radarToolsPosX - config.dimensions['width'] - 11
    y0 = radarToolsPosY - 50
    radarCenterX = x0 + config.dimensions['halfWidth']
    radarCenterY = y0 + config.dimensions['halfHeight']
    (playerPixelCoordinateX, playerPixelCoordinateY) = utils.core.getPixelFromCoordinate(
        playerCoordinate)
    (destinationPixelCoordinateX,
     destinationPixelCoordinateY) = utils.core.getPixelFromCoordinate(coordinate)
    x = destinationPixelCoordinateX - playerPixelCoordinateX + radarCenterX
    y = destinationPixelCoordinateY - playerPixelCoordinateY + radarCenterY
    pyautogui.click(x, y)
    sleep(0.25)


def isCloseToCoordinate(currentCoordinate, possibleCloseCoordinate, distanceTolerance=10):
    (xOfCurrentCoordinate, yOfCurrentCoordinate, _) = currentCoordinate
    (xOfPossibleCloseCoordinate, yOfPossibleCloseCoordinate, _) = possibleCloseCoordinate
    distanceOfXAxis = abs(xOfCurrentCoordinate - xOfPossibleCloseCoordinate)
    distanceOfYAxis = abs(yOfCurrentCoordinate - yOfPossibleCloseCoordinate)
    isClose = distanceOfXAxis <= distanceTolerance and distanceOfYAxis <= distanceTolerance
    return isClose


def isCoordinateWalkable(coordinate):
    (x, y) = utils.core.getPixelFromCoordinate(coordinate)
    walkable = config.walkableFloorsSqms[y, x]
    return walkable


def isNonWalkablePixelColor(pixelColor):
    return np.isin(pixelColor, config.nonWalkablePixelsColors)