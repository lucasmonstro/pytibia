from time import sleep

import cv2
import numpy as np
import pyautogui
import utils.core
import utils.image
import radar.core

accessoriesEquippedImg = utils.image.loadAsArray('radar/images/radar-tools.png')
hpImg = utils.image.loadAsArray('player/images/heart.png')
manaImg = utils.image.loadAsArray('player/images/mana.png')
bleedingImg = utils.image.loadAsArray('player/images/bleeding.png')
cursedImg = utils.image.loadAsArray('player/images/cursed.png')
burningImg = utils.image.loadAsArray('player/images/burning.png')
fightImg = utils.image.loadAsArray('player/images/fight.png')
hungryImg = utils.image.loadAsArray('player/images/hungry.png')
poisonedImg = utils.image.loadAsArray('player/images/poisoned.png')
pzImg = utils.image.loadAsArray('player/images/pz.png')
restingAreaImg = utils.image.loadAsArray('player/images/resting-area.png')
stopImg = utils.image.loadAsArray('player/images/stop.png')
emptyArmorImg = utils.image.loadAsArray('player/images/empty-armor.png')
emptyBeltImg = utils.image.loadAsArray('player/images/empty-arrow.png')
emptyBackPackImg = utils.image.loadAsArray('player/images/empty-backpack.png')
emptyBootsImg = utils.image.loadAsArray('player/images/empty-boots.png')
emptyHelmetImg = utils.image.loadAsArray('player/images/empty-helmet.png')
emptyLegsIms = utils.image.loadAsArray('player/images/empty-legs.png')
emptyNecklaceImg = utils.image.loadAsArray('player/images/empty-necklace.png')
emptyRingImg = utils.image.loadAsArray('player/images/empty-ring.png')
emptyShieldImg = utils.image.loadAsArray('player/images/empty-shield.png')
emptyWeaponImg = utils.image.loadAsArray('player/images/empty-weapon.png')
followingAttackDisImg = utils.image.loadAsArray('player/images/following-attack-disabled.png')
balancedAttackImg = utils.image.loadAsArray('player/images/balanced-attack.png')
defensiveAttackImg = utils.image.loadAsArray('player/images/defensive-attack.png')
fullAttackImg = utils.image.loadAsArray('player/images/full-attack.png')
drunkImg = utils.image.loadAsArray('player/images/drunk.png')
electrifiedImg = utils.image.loadAsArray('player/images/eletrified.png')
followingAttackImg = utils.image.loadAsArray('player/images/following-attack.png')
hasteImg = utils.image.loadAsArray('player/images/haste.png')
holdingAttackImg = utils.image.loadAsArray('player/images/holding-attack.png')
inventoryHiddenImg = utils.image.loadAsArray('player/images/inventory-hidden.png')
logoutBlockImg = utils.image.loadAsArray('player/images/logout-block.png')
readyForPvpImg = utils.image.loadAsArray('player/images/ready-for-pvp.png')
slowedImg = utils.image.loadAsArray('player/images/slowed.png')
storeImg = utils.image.loadAsArray('player/images/store.png')

hpBarAllowedPixelsColors = np.array([79, 118, 121, 110, 62])
hpBarSize = 94

manaBarAllowedPixelsColors = np.array([68, 95, 97, 89, 52])
manaBarSize = 94


def getFilledBarPercentage(bar, size=100, allowedPixelsColors=[]):
    bar = np.where(np.isin(bar, allowedPixelsColors), 0, bar)
    barPercent = np.count_nonzero(bar == 0)
    percent = (barPercent * 100 // size)
    return percent


@utils.core.cacheObjectPos
def getHeartPos(screenshot):
    return utils.core.locate(screenshot, hpImg)


def getHealthPercentage(screenshot):
    heartPos = getHeartPos(screenshot)
    didntGetHpPos = heartPos == None
    if didntGetHpPos:
        return None
    bar = getHealthBar(screenshot, heartPos)
    percent = getFilledBarPercentage(bar, size=hpBarSize,
                                     allowedPixelsColors=hpBarAllowedPixelsColors)
    return percent


def getHealthBar(screenshot, heartPos):
    (left, top, _, _) = heartPos
    y0 = top + 5
    y1 = y0 + 1
    x0 = left + 13
    x1 = x0 + hpBarSize
    bar = screenshot[y0:y1, x0:x1][0]
    return bar


@utils.core.cacheObjectPos
def getManaPos(screenshot):
    return utils.core.locate(screenshot, manaImg)


def getManaPercentage(screenshot):
    manaPos = getManaPos(screenshot)
    didntGetHpPos = manaPos is None
    if didntGetHpPos:
        return None
    bar = getManaBar(screenshot, manaPos)
    percent = getFilledBarPercentage(bar, size=manaBarSize,
                                     allowedPixelsColors=manaBarAllowedPixelsColors)
    return percent


def getManaBar(screenshot, heartPos):
    (left, top, _, _) = heartPos
    y0 = top + 5
    y1 = y0 + 1
    x0 = left + 14
    x1 = x0 + manaBarSize
    bar = screenshot[y0:y1, x0:x1][0]
    return bar


@utils.core.cacheObjectPos
def getStopPos(screenshot):
    return utils.core.locate(screenshot, stopImg)


def getFightStatusContainer(screenshot, slotName):
    (left, top, _, _) = getStopPos(screenshot)
    fightStatusImgList = {
        'defensive-attack': (screenshot[top - 98: top - 98 + 30, left:left + 30], left, top - 98),
        'balanced-attack': (screenshot[top - 123: top - 123 + 30, left:left + 30], left, top - 123),
        'full-attack': (screenshot[top - 144: top - 144 + 30, left:left + 30], left, top - 144),
        'holding-attack': (screenshot[top - 144: top - 144 + 30, left + 22: left + 22 + 30], left + 22, top - 144),
        'following-attack': (screenshot[top - 123: top - 123 + 30, left + 22: left + 22 + 30], left + 22, top - 123)
    }

    fightStatusImg = fightStatusImgList.get(slotName, None)
    return fightStatusImg


def setFightStatus(screenshot, statusName):
    (container, x, y) = getFightStatusContainer(screenshot, statusName)

    fightStatusList = {
        'defensive-attack': defensiveAttackImg,
        'balanced-attack': balancedAttackImg,
        'full-attack': fullAttackImg,
        'holding-attack': holdingAttackImg,
        'following-attack': followingAttackImg
    }

    statusImg = fightStatusList.get(statusName, None)
    pos = utils.core.locate(container, statusImg)
    if pos is None:
        print('Enabling fight status: ' + statusName)
        pyautogui.click(x + 10, y + 10)


def getReadyForPvpContainer(screenshot):
    (left, top, _, _) = getStopPos(screenshot)
    top -= 72
    return screenshot[top: top + 20, left:left + 42], left, top


def setReadyForPvp(screenshot, condition):

    (pvpBtn, left, top) = getReadyForPvpContainer(screenshot)
    pos = utils.core.locate(pvpBtn, readyForPvpImg, 0.5)
    actualStatus = pos is not None

    if condition != actualStatus:
        print('Changing PVP status to: ' + str(condition))
        pyautogui.click(left + 10, top + 10)


def getEquipmentContainer(screenshot, slotName):
    (left, top, _, _) = getStopPos(screenshot)
    equipList = {
        'backpack': (left - 42, top - 128),
        'helmet': (left - 79, top - 142),
        'necklace': (left - 116, top - 128),
        'weapon': (left - 116, top - 92),
        'shield': (left - 42, top - 92),
        'armor': (left - 79, top - 106),
        'ring': (left - 116, top - 56),
        'legs': (left - 79, top - 70),
        'boots': (left - 79, top - 34),
        'belt': (left - 42, top - 56)
    }
    (x, y) = equipList.get(slotName, None)
    return screenshot[y:y + 30, x:x + 30]


def isEquipmentEquipped(screenshot, equipment):
    container = getEquipmentContainer(screenshot, equipment)
    emptyImgList = {
        'backpack': emptyBackPackImg,
        'helmet': emptyHelmetImg,
        'necklace': emptyNecklaceImg,
        'weapon': emptyWeaponImg,
        'shield': emptyShieldImg,
        'armor': emptyArmorImg,
        'ring': emptyRingImg,
        'legs': emptyLegsIms,
        'boots': emptyBootsImg,
        'belt': emptyBeltImg
    }

    emptyImg = emptyImgList.get(equipment, None)
    pos = utils.core.locate(container, emptyImg)
    cond = pos is None
    return cond


def getSpecialConditionsContainer(screenshot):
    (left, top, _, _) = getStopPos(screenshot)
    container = screenshot[top:top + 12, left - 118:left - 118 + 107]
    return container


def hasSpecialCondition(screenshot, condition):
    container = getSpecialConditionsContainer(screenshot)

    condList = {
        'bleeding': bleedingImg,
        'burning': burningImg,
        'cursed': cursedImg,
        'hungry': hungryImg,
        'fight': fightImg,
        'pz': pzImg,
        'restingArea': restingAreaImg,
        'poisoned': poisonedImg,
        'drunk': drunkImg,
        'electrified': electrifiedImg,
        'haste': hasteImg,
        'slowed': slowedImg,
        'logoutBlock': logoutBlockImg
    }

    compareImg = condList.get(condition, None)
    pos = utils.core.locate(container, compareImg)
    cond = pos is not None
    return cond


def setInventoryVisible(screenshot, condition):
    pos = utils.core.locate(screenshot, storeImg)
    inventoryVisible = pos is not None
    if inventoryVisible == condition:
        return
    print('Changing show inventory status to: ' + str(condition))
    if pos is None:
        (left, top, _, _) = radar.core.getRadarToolsPos(screenshot)
        left -= 118
        top += 64
        pyautogui.click(x=left + 6, y=top + 6)
    else:
        pyautogui.click(x=pos[0] - 74, y=pos[1] + 6)


def stop(seconds=1):
    pyautogui.press('esc')
    sleep(seconds)
