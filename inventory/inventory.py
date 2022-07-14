import time
import pyautogui
from utils import utils

backpackBarImg = utils.loadImgAsArray('inventory/images/backpackBar.png')
jewelledBackpackBarImg = utils.loadImgAsArray('inventory/images/jewelledBackpackBar.png')
blueBackpackBarImg = utils.loadImgAsArray('inventory/images/blueBackpackBar.png')
orangeBackpackBarImg = utils.loadImgAsArray('inventory/images/orangeBackpackBar.png')
backpackBottomImg = utils.loadImgAsArray('inventory/images/backpackBottom.png')
mainBackpackImg = utils.loadImgAsArray('inventory/images/mainBackpack.png')
lockerBarImg = utils.loadImgAsArray('inventory/images/lockerBar.png')
depotBarImg = utils.loadImgAsArray('inventory/images/depotBar.png')

jewelledBpItems = [
    'great-health-potion',
    'great-mana-potion',
    'great-spirit-potion',
    'health-potion',
    'mana-potion',
    'strong-health-potion',
    'strong-mana-potion',
    'ultimate-health-potion'
    'ultimate-mana-potion',
    'ultimate-spirit-potion'
]

itemsImgs = [
    ('great-health-potion', utils.loadColoredImg('inventory/images/items/great-health-potion.png')),
    ('great-mana-potion', utils.loadColoredImg('inventory/images/items/great-mana-potion.png')),
    ('great-spirit-potion', utils.loadColoredImg('inventory/images/items/great-spirit-potion.png')),
    ('health-potion', utils.loadColoredImg('inventory/images/items/health-potion.png')),
    ('mana-potion', utils.loadColoredImg('inventory/images/items/mana-potion.png')),
    ('strong-health-potion', utils.loadColoredImg('inventory/images/items/strong-health-potion.png')),
    ('strong-mana-potion', utils.loadColoredImg('inventory/images/items/strong-mana-potion.png')),
    ('ultimate-health-potion', utils.loadColoredImg('inventory/images/items/ultimate-health-potion-1.png')),
    ('ultimate-health-potion', utils.loadColoredImg('inventory/images/items/ultimate-health-potion-2.png')),
    ('ultimate-health-potion', utils.loadColoredImg('inventory/images/items/ultimate-health-potion-3.png')),
    ('ultimate-health-potion', utils.loadColoredImg('inventory/images/items/ultimate-health-potion-4.png')),
    ('ultimate-health-potion', utils.loadColoredImg('inventory/images/items/ultimate-health-potion-5.png')),
    ('ultimate-health-potion', utils.loadColoredImg('inventory/images/items/ultimate-health-potion-6.png')),
    ('ultimate-health-potion', utils.loadColoredImg('inventory/images/items/ultimate-health-potion-7.png')),
    ('ultimate-mana-potion', utils.loadColoredImg('inventory/images/items/ultimate-mana-potion-1.png')),
    ('ultimate-mana-potion', utils.loadColoredImg('inventory/images/items/ultimate-mana-potion-2.png')),
    ('ultimate-mana-potion', utils.loadColoredImg('inventory/images/items/ultimate-mana-potion-3.png')),
    ('ultimate-mana-potion', utils.loadColoredImg('inventory/images/items/ultimate-mana-potion-4.png')),
    ('ultimate-mana-potion', utils.loadColoredImg('inventory/images/items/ultimate-mana-potion-5.png')),
    ('ultimate-mana-potion', utils.loadColoredImg('inventory/images/items/ultimate-mana-potion-6.png')),
    ('ultimate-spirit-potion', utils.loadColoredImg('inventory/images/items/ultimate-spirit-potion-1.png')),
    ('ultimate-spirit-potion', utils.loadColoredImg('inventory/images/items/ultimate-spirit-potion-2.png')),
    ('ultimate-spirit-potion', utils.loadColoredImg('inventory/images/items/ultimate-spirit-potion-3.png')),
    ('ultimate-spirit-potion', utils.loadColoredImg('inventory/images/items/ultimate-spirit-potion-4.png')),
    ('ultimate-spirit-potion', utils.loadColoredImg('inventory/images/items/ultimate-spirit-potion-5.png')),
    ('ultimate-spirit-potion', utils.loadColoredImg('inventory/images/items/ultimate-spirit-potion-6.png')),
    ('ultimate-spirit-potion', utils.loadColoredImg('inventory/images/items/ultimate-spirit-potion-7.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-1.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-2.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-3.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-4.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-5.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-6.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-7.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-8.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-9.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-10.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-11.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-12.png')),
    ('supreme-health-potion', utils.loadColoredImg('inventory/images/items/supreme-health-potion-13.png')),
    ('brown-backpack', utils.loadColoredImg('inventory/images/items/brown-backpack.png')),
    ('blue-backpack', utils.loadColoredImg('inventory/images/items/blue-backpack.png')),
    ('orange-backpack', utils.loadColoredImg('inventory/images/items/orange-backpack.png')),
    ('jewelled-backpack', utils.loadColoredImg('inventory/images/items/jewelled-backpack.png')),
    ('shopping-bag', utils.loadColoredImg('inventory/images/items/shopping-bag.png')),
    ('depot-chest-1', utils.loadColoredImg('inventory/images/items/depot-chest-1.png')),
    ('depot-chest-2', utils.loadColoredImg('inventory/images/items/depot-chest-2.png')),
    ('depot-chest-3', utils.loadColoredImg('inventory/images/items/depot-chest-3.png')),
    ('depot-chest-4', utils.loadColoredImg('inventory/images/items/depot-chest-4.png')),
    ('depot-chest-5', utils.loadColoredImg('inventory/images/items/depot-chest-5.png')),
    ('depot-chest-6', utils.loadColoredImg('inventory/images/items/depot-chest-6.png')),
    ('depot-chest-7', utils.loadColoredImg('inventory/images/items/depot-chest-7.png')),
    ('depot-chest-8', utils.loadColoredImg('inventory/images/items/depot-chest-8.png')),
    ('depot-chest-9', utils.loadColoredImg('inventory/images/items/depot-chest-9.png')),
    ('depot-chest-10', utils.loadColoredImg('inventory/images/items/depot-chest-10.png')),
    ('depot-chest-11', utils.loadColoredImg('inventory/images/items/depot-chest-11.png')),
    ('depot-chest-12', utils.loadColoredImg('inventory/images/items/depot-chest-12.png')),
    ('depot-chest-13', utils.loadColoredImg('inventory/images/items/depot-chest-13.png')),
    ('depot-chest-14', utils.loadColoredImg('inventory/images/items/depot-chest-14.png')),
    ('depot-chest-15', utils.loadColoredImg('inventory/images/items/depot-chest-15.png')),
    ('depot-chest-16', utils.loadColoredImg('inventory/images/items/depot-chest-16.png')),
    ('depot-chest-17', utils.loadColoredImg('inventory/images/items/depot-chest-17.png')),
    ('depot-chest-18', utils.loadColoredImg('inventory/images/items/depot-chest-18.png')),
    ('empty', utils.loadColoredImg('inventory/images/items/empty.png')),
]


def getWindowTopPos(screenshot, img):
    return utils.locate(screenshot, img)


def getWindowBottomPos(screenshot, topPos):
    (x, y, w, h) = topPos
    (botX, botY, width, height) = utils.locate(utils.cropImg(screenshot, x, y, 160, 250), backpackBottomImg)
    return x, y + botY, 172, 1


def adjustAndGetWindowPos(window, img, squares):
    screenshot = utils.getScreenshot(window)
    (x0, y0, w0, h0) = getWindowTopPos(screenshot, img)
    (x1, y1, w1, h1) = getWindowBottomPos(screenshot, (x0, y0, w0, h0))

    incompleteLine = 0
    if (squares % 4) != 0:
        incompleteLine = 1
    maxWindowSize = 14 + (36 * ((squares // 4) + incompleteLine)) + 12
    if (y1 - y0) < maxWindowSize:
        utils.mouseDrag(x0 + 70, y1, x0 + 70, y1 + (maxWindowSize - (y1 - y0)))
        screenshot = utils.getScreenshot(window)
        (x1, y1, w1, h1) = getWindowBottomPos(screenshot, (x0, y0, w0, h0))
        return x0, y0, w0, y1 - y0
    return x0, y0, w0, y1 - y0


def isWindowOpen(screenshot, windowBar):
    backpackPos = utils.locate(screenshot, windowBar)
    if backpackPos is None:
        return False
    return True


def openMainBackpack(window, squares):
    screenshot = utils.getScreenshot(window)
    (x, y, w, h) = utils.locate(screenshot, mainBackpackImg)
    if isWindowOpen(screenshot, backpackBarImg) is False:
        (xBp, yBp) = utils.randomCoord(x + 3, y + 18, w - 3, h - 25)
        utils.rightClick(xBp, yBp)
        time.sleep(1)
    backpackPos = adjustAndGetWindowPos(window, backpackBarImg, squares)
    backpackMap = mapWindowSquares(window, backpackPos, squares)
    return backpackPos, backpackMap


def mapWindowSquares(window, windowPos, squares):
    screenshot = utils.getColoredScreenshot(window)
    (x, y, w, h) = windowPos
    containerMap = []
    (borX, borY) = (11, 20)
    incompleteLine = 0
    if (squares % 4) != 0:
        incompleteLine = 1
    for i in range((squares // 4) + incompleteLine):
        for j in range(4):
            squarePos = (x + borX + 32 * j + 5 * j, y + borY + 32 * i + 5 * i)
            itemName = 'unknown'
            for k in range(len(itemsImgs)):
                (listH, listW, listC) = itemsImgs[k][1].shape
                itemFound = utils.locate(
                    utils.cropImg(screenshot, squarePos[0] + 2, squarePos[1] + 1, 32 - 4, listH - 1), itemsImgs[k][1],
                    0.95)
                if itemFound is not None:
                    itemName = itemsImgs[k][0]
                    break
            if len(containerMap) < squares:
                containerMap.append((itemName, squarePos[0], squarePos[1]))

    return containerMap


def openDepot(window):
    screenshot = utils.getScreenshot(window)
    (x, y, w, h) = utils.locate(screenshot, lockerBarImg)
    (xLck, yLck) = utils.randomCoord(x + 11, y + 20, 28, 28)
    utils.rightClick(xLck, yLck)
    time.sleep(1)
    DepotPos = adjustAndGetWindowPos(window, depotBarImg, 18)
    DepotMap = mapWindowSquares(window, DepotPos, 18)
    return DepotPos, DepotMap


def closeWindow(windowPos):
    (x, y, w, h) = windowPos
    clickCoord = utils.randomCoord(x + 162, y + 4, 10, 10)
    pyautogui.click(clickCoord[0], clickCoord[1])


def moveItem(fromContainerMap, toContainerMap, slotIndex):
    if toContainerMap[len(toContainerMap)-1][0] != 'empty':
        return None

    fromPos = utils.randomCoord(fromContainerMap[slotIndex][1], fromContainerMap[slotIndex][2], 28, 28)
    toPos = utils.randomCoord(toContainerMap[0][1], toContainerMap[0][2], 28, 28)
    utils.mouseDrag(fromPos[0], fromPos[1], toPos[0], toPos[1])

    for i in reversed(range(1, len(toContainerMap))):
        toContainerMap[i] = (toContainerMap[i - 1][0], toContainerMap[i][1], toContainerMap[i][2])
    toContainerMap[0] = (fromContainerMap[slotIndex][0], toContainerMap[0][1], toContainerMap[0][2])

    for i in range(slotIndex, len(fromContainerMap) - 1):
        fromContainerMap[i] = (fromContainerMap[i + 1][0], fromContainerMap[i][1], fromContainerMap[i][2])
    fromContainerMap[len(fromContainerMap)-1] = ('empty', fromContainerMap[len(fromContainerMap)-1][1], fromContainerMap[len(fromContainerMap)-1][2])

    return fromContainerMap, toContainerMap
