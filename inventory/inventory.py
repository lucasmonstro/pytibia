import time
from utils import utils

backpackBarImg = utils.loadImgAsArray('inventory/images/backpackBar.png')
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
    ('ultimate-health-potion', utils.loadColoredImg('inventory/images/items/ultimate-health-potion.png')),
    ('ultimate-mana-potion', utils.loadColoredImg('inventory/images/items/ultimate-mana-potion.png')),
    ('ultimate-spirit-potion', utils.loadColoredImg('inventory/images/items/ultimate-spirit-potion.png')),
    ('normal-backpack', utils.loadColoredImg('inventory/images/items/normal-backpack.png')),
    ('jewelled-backpack', utils.loadColoredImg('inventory/images/items/jewelled-backpack.png')),
    ('shopping-bag', utils.loadColoredImg('inventory/images/items/shopping-bag.png')),
]


def getWindowTopPos(screenshot, img):
    return utils.locate(screenshot, img)


def getWindowBottomPos(screenshot, topPos):
    (x, y, w, h) = topPos
    (botX, botY, width, height) = utils.locate(utils.cropImg(screenshot, x, y, 160, 250), backpackBottomImg)
    return x, y + botY, 172, 1


def adjustAndGetWindowPos(window, img):
    screenshot = utils.getScreenshot(window)
    (x0, y0, w0, h0) = getWindowTopPos(screenshot, img)
    (x1, y1, w1, h1) = getWindowBottomPos(screenshot, (x0, y0, w0, h0))

    if (y1 - y0) < 209:
        utils.mouseDrag(x0 + 70, y1, x0 + 70, y1 + (212 - (y1 - y0)))
        screenshot = utils.getScreenshot(window)
        (x1, y1, w1, h1) = getWindowBottomPos(screenshot, (x0, y0, w0, h0))
        return x0, y0, w0, y1 - y0
    return x0, y0, w0, y1 - y0


def isBackpackOpen(screenshot):
    backpackPos = utils.locate(screenshot, backpackBarImg)
    if backpackPos is None:
        return False
    return True


def openMainBackpack(window):
    screenshot = utils.getScreenshot(window)
    (x, y, w, h) = utils.locate(screenshot, mainBackpackImg)
    if isBackpackOpen(screenshot) is False:
        (xBp, yBp) = utils.randomCoord(x + 3, y + 18, w - 3, h - 25)
        utils.rightClick(xBp, yBp)
        time.sleep(1)
    backpackPos = adjustAndGetWindowPos(window, backpackBarImg)
    backpackMap = mapWindowSquares(window, backpackPos)
    return backpackPos, backpackMap


def mapWindowSquares(window, backpackPos):
    screenshot = utils.getColoredScreenshot(window)
    (x, y, w, h) = backpackPos
    containerMap = []
    (borX, borY) = (11, 20)
    for i in range(5):
        for j in range(4):
            squarePos = (x + borX + 32 * j + 5 * j, y + borY + 32 * i + 5 * i)
            itemName = 'unknown'
            for k in range(len(itemsImgs)):
                (listH, listW, listC) = itemsImgs[k][1].shape
                itemFound = utils.locate(utils.cropImg(screenshot, squarePos[0]+2, squarePos[1]+1, 32 - 4, listH - 1), itemsImgs[k][1], 0.98)
                if itemFound is not None:
                    itemName = itemsImgs[k][0]
                    break
            containerMap.append((itemName, squarePos[0], squarePos[1]))

    return containerMap


def openDepot(window):
    screenshot = utils.getScreenshot(window)
    (x, y, w, h) = utils.locate(screenshot, lockerBarImg)
    (xLck, yLck) = utils.randomCoord(x + 11, y + 20, 28, 28)
    utils.rightClick(xLck, yLck)
    time.sleep(1)
    DepotPos = adjustAndGetWindowPos(window, depotBarImg)
    DepotMap = mapWindowSquares(DepotPos)
    return [DepotPos, DepotMap]
