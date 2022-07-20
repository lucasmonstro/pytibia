from actionBar import cooldown
import battleList.core
import hud.creatures
import player.core
import radar.core
import utils.core, utils.image
from rx import operators
from rx.scheduler import ThreadPoolScheduler
import numpy as np
import rx
import time
import pygetwindow as gw
import multiprocessing

# import sys
# np.set_printoptions(threshold=sys.maxsize)

waypointType = np.dtype([
    ('type', np.str_, 64),
    ('coordinate', np.uint32, (3,)),
    ('tolerance', np.uint8)
])
waypoints = np.array([
    ('floor', (33085, 32788, 7), 0),
    ('ramp', (33085, 32786, 6), 0),
    ('floor', (33085, 32785, 6), 0),
    ('ramp', (33085, 32783, 7), 0),
    ('floor', (33038, 32810, 7), 0),
    ('ramp', (33038, 32808, 6), 0),
    ('floor', (33033, 32801, 6), 0),
    ('ramp', (33033, 32799, 5), 0),
    ('floor', (33032, 32779, 5), 0),
    ('ramp', (33032, 32777, 4), 0),
    ('floor', (33032, 32786, 4), 0),
    ('ramp', (33032, 32788, 3), 0),
    ('floor', (33031, 32788, 3), 0),
    ('ramp', (33029, 32788, 2), 0),
    ('floor', (33029, 32781, 2), 0),
    ('ramp', (33029, 32779, 1), 0),
    ('floor', (33029, 32776, 1), 0),
    ('ramp', (33029, 32774, 0), 0),
    ('floor', (33030, 32756, 0), 0),
    ('ramp', (33032, 32756, 1), 0),
    ('floor', (33021, 32746, 1), 0),
    ('ramp', (33019, 32746, 2), 0),
    ('floor', (33016, 32745, 2), 0),
    ('ramp', (33016, 32743, 3), 0),
    ('floor', (33010, 32727, 3), 0),
    ('ramp', (33010, 32725, 4), 0),
    ('floor', (32999, 32703, 4), 0),
    ('ramp', (32999, 32705, 5), 0),
    ('floor', (32998, 32709, 5), 0),
    ('ramp', (32998, 32711, 6), 0),
    ('floor', (32982, 32715, 6), 0),
    ('ramp', (32982, 32717, 7), 0),
    ('floor', (32953, 32769, 7), 0),

    ('floor', (32953, 32785, 7), 0),
    ('floor', (32959, 32785, 7), 0),

    ('floor', (33004, 32750, 7), 0),
    ('ramp', (33006, 32750, 6), 0),
    ('floor', (33015, 32749, 6), 0),
    ('ramp', (33015, 32751, 5), 0),
    ('ramp', (33015, 32753, 4), 0),
    ('floor', (33009, 32770, 4), 0),
    ('ramp', (33009, 32772, 5), 0),
    ('floor', (33004, 32765, 5), 0),
    ('ramp', (33004, 32767, 6), 0),
    ('floor', (33004, 32770, 6), 0),
    ('ramp', (33004, 32772, 7), 0),
    ('floor', (33004, 32772, 7), 10),
    ('floor', (32994, 32815, 7), 10),
    ('floor', (33003, 32831, 7), 10),
    ('floor', (32975, 32802, 7), 10),
    ('floor', (32957, 32824, 7), 10),
    ('floor', (32978, 32832, 7), 10),
    ('floor', (32981, 32857, 7), 10),
    ('floor', (32961, 32861, 7), 10),
    ('floor', (32958, 32834, 7), 10),
    ('floor', (32987, 32799, 7), 10),
    # ('floor', (32981, 32795, 7)),
    # ('floor', (32962, 32814, 7)),
    # ('floor', (32996, 32805, 7)),
    # ('floor', (33005, 32783, 7)),
], dtype=waypointType)

# waypoints = np.array([
#     ('floor', (33871, 31457, 7), 0),
#     ('floor', (33875, 31441, 7), 0),
#     ('floor', (33850, 31457, 7), 0),
#     ('floor', (33828, 31473, 7), 0),
#     ('floor', (33842, 31500, 7), 0),
# ], dtype=waypointType)

# waypoints = np.array([
#     ('floor', (33538, 32475, 7), 0),
#     ('floor', (33530, 32470, 7), 0),
#     ('floor', (33509, 32480, 7), 0),
#     ('floor', (33526, 32452, 7), 0),
#     ('floor', (33550, 32445, 7), 0),
#     ('floor', (33571, 32456, 7), 0),
# ], dtype=waypointType)
waypointIndex = None
shouldIgnoreTargetAndGoToNextWaypoint = False
shouldRetrySameWaypoint = True
window = None
targetIsEnabled = False


def goToWaypoint(screenshot, waypoint, currentPlayerCoordinate):
    global shouldIgnoreTargetAndGoToNextWaypoint
    print('setting shouldIgnoreTargetAndGoToNextWaypoint to false')
    shouldIgnoreTargetAndGoToNextWaypoint = False
    isFloorWaypoint = waypoint['type'] == 'floor'
    if isFloorWaypoint:
        radar.core.goToCoordinate(screenshot, currentPlayerCoordinate, waypoint['coordinate'])
        return
    isRampWaypoint = waypoint['type'] == 'ramp'
    if isRampWaypoint:
        (currentPlayerCoordinateX, currentPlayerCoordinateY, _) = currentPlayerCoordinate
        (waypointCoordinateX, waypointCoordinateY, _) = waypoint['coordinate']
        xDifference = currentPlayerCoordinateX - waypointCoordinateX
        shouldWalkToLeft = xDifference > 0
        if shouldWalkToLeft:
            utils.core.press('left')
            return
        shouldWalkToRight = xDifference < 0
        if shouldWalkToRight:
            utils.core.press('right')
            return
        yDifference = currentPlayerCoordinateY - waypointCoordinateY
        if yDifference < 0:
            utils.core.press('down')
            return
        if yDifference > 0:
            utils.core.press('up')
            return


def handleCavebot(screenshot, playerCoordinate, battleListCreatures, hudCreatures):
    global shouldIgnoreTargetAndGoToNextWaypoint, shouldRetrySameWaypoint
    shouldRetrySameWaypoint = True
    hasNoHudCreatures = len(hudCreatures) == 0
    if hasNoHudCreatures:
        print('has no hud creatures')
        return
    # if battleList.isAttackingCreature(battleListCreatures):
    #     # obter a matriz do mapa
    #     # obter as coordenadas das creatures
    #     # marcar as coordenadas das creatures com 0
    #     # marcar a coordenada do target com 1
    #     hudWalkableFloorsSqms = radar.config.walkableFloorsSqms[playerCoordinate[2]]
    #     hudwalkableFloorsSqms = hudWalkableFloorsSqms[y-5:y+6, x-7:x+8]
    #     for creature in hudCreatures:
    #         hudwalkableFloorsSqms[creature['slot'][1], creature['slot'][0]] = 0
    #     # get closest creature index
    #     creatureIndex = [10, 6]
    #     hasTargetToCreatureByIndex = hud.creatures.hasTargetToCreatureByIndex(hudwalkableFloorsSqms, creatureIndex)
    #     print(hasTargetToCreatureByIndex)
    #     return
    closestCreature = hud.creatures.getClosestCreature(hudCreatures, playerCoordinate,
                                                       radar.core.config.walkableFloorsSqms[playerCoordinate[2]])
    hasNoClosestCreature = closestCreature == None
    if hasNoClosestCreature:
        print('has no closest creature')
        shouldIgnoreTargetAndGoToNextWaypoint = True
        return
    (x, y) = closestCreature['windowCoordinate']
    utils.core.rightClick(x, y)
    time.sleep(0.25)


def handleWaypoints(screenshot, coordinate):
    global shouldRetrySameWaypoint, waypointIndex
    if waypointIndex == None:
        waypointIndex = radar.core.getWaypointIndexFromClosestCoordinate(coordinate, waypoints)
    currentWaypoint = waypoints[waypointIndex]
    isCloseToCoordinate = radar.core.isCloseToCoordinate(
        coordinate, waypoints[waypointIndex]['coordinate'],
        distanceTolerance=currentWaypoint['tolerance'])
    # print(isCloseToCoordinate)
    # print('aeeeeee')
    if isCloseToCoordinate:
        waypointIndex = 0 if waypointIndex == len(
            waypoints) - 1 else waypointIndex + 1
        shouldRetrySameWaypoint = False
        player.core.stop(0.5)
        # Verificar se tem caminho
        # 1. Pegar a distancia entre x0 e x1
        # (radarCoordinateX, radarCoordinateY, floorLevel) = coordinate
        # print('radarCoordinateX', radarCoordinateX)
        # print('radarCoordinateY', radarCoordinateY)
        # (pixelCoordinateX, pixelCoordinateY) = utils.getPixelFromCoordinate(coordinate)
        # print('pixelCoordinateX', pixelCoordinateX)
        # print('pixelCoordinateY', pixelCoordinateY)
        # print(radar.config.walkableFloorsSqms[floorLevel, y-22:y+22, x-7-15:x+8+15])
        # bolas = radar.config.walkableFloorsSqms[floorLevel][pixelCoordinateY-22:pixelCoordinateY+23, pixelCoordinateX-22:pixelCoordinateX+23]
        # bolas = np.where(bolas == 1, 255, 0)
        # bolas = np.array(bolas, dtype=np.uint8)
        # bolas[22][23] = 133
        # utils.image.saveFromArray(bolas, 'bolas.png')
        # adjacencyMatrix = utils.getAdjacencyMatrix(bolas)
        # sqmsGraph = csr_matrix(adjacencyMatrix)
        # print(sqmsGraph)
        # sqmsGraphWeights = dijkstra(sqmsGraph, directed=True, indices=1014, unweighted=False)
        # print('sqmsGraphWeights', sqmsGraphWeights)
        # print(sqmsGraphWeights.reshape(45, 45))
        # print('weight', sqmsGraphWeights[1019])
        # creaturesIndexes = np.nonzero(bolas.flatten() == 1)[0]
        # creaturesWeights = np.take(sqmsGraphWeights, creaturesIndexes)
        # fa = utils.image.loadAsArray('hud/images/monsters/Abyssador.png')
        # print(fa)
        # bolas = np.array(bolas, dtype=np.uint8)
        # utils.image.saveFromArray(fa, 'fa.png')
        # print(bolas)
        # utils.image.saveFromArray(bolas, 'bolas.png')
        # abs(waypoints[waypointIndex]['coordinate'][0] - coordinate[0])
        # Pegar a distancia enter y0 e y1
        # Gerar um retangulo a partir de radar.config.walkableFloorsSqms[playerCoordinate[2]]
        # Mesclar a hud no retangulo
        # return
        goToWaypoint(screenshot, waypoints[waypointIndex], coordinate)
        return
    if shouldRetrySameWaypoint:
        shouldRetrySameWaypoint = False
        player.core.stop(0.5)
        if (currentWaypoint['type'] == 'ramp'):
            waypointIndex = waypointIndex + 1
            currentWaypoint = waypoints[waypointIndex]
        goToWaypoint(screenshot, currentWaypoint, coordinate)


def handleHealing(healthPercentage, manaPercentage):
    percentageToHealWithManaPotion = 65
    percentageToHealWithPotion = 70
    percentageToHealWithSpell = 75
    spellHotkey = 'f3'
    manaPotionHotkey = 'f2'
    healthPotionHotkey = 'f1'
    shouldHealWithHealthPotion = healthPercentage < percentageToHealWithPotion
    if shouldHealWithHealthPotion:
        print('healing with health potion...')
        utils.core.press(healthPotionHotkey)
        time.sleep(0.25)
        return
    shouldHealWithMana = manaPercentage < percentageToHealWithManaPotion
    if shouldHealWithMana:
        print('healing with mana potion...')
        utils.core.press(manaPotionHotkey)
        time.sleep(0.25)
        return
    # shouldHealWithSpell = healthPercentage < percentageToHealWithSpell or manaPercentage > 90
    # if shouldHealWithSpell:
    #     print('healing with spell...')
    #     utils.press(spellHotkey)
    #     time.sleep(0.25)


def getWindow():
    targetWindowTitle = None
    allTitles = gw.getAllTitles()
    for title in allTitles:
        if title.startswith('Tibia -'):
            targetWindowTitle = title
    hasNoTargetWindowTitle = targetWindowTitle == None
    if hasNoTargetWindowTitle:
        return None
    windowTitles = gw.getWindowsWithTitle(targetWindowTitle)
    hasNoWindowsMatchingTitles = len(windowTitles) == 0
    if hasNoWindowsMatchingTitles:
        return None
    return windowTitles[0]


def handleWindow(_):
    global window
    windowIsEmpty = window is None
    if windowIsEmpty:
        window = getWindow()
    return window


def handleSpell(screenshot, hudCreatures):
    nearestCreaturesCount = hud.creatures.getNearestCreaturesCount(hudCreatures)
    hasNoNearestCreatures = nearestCreaturesCount == 0
    if hasNoNearestCreatures:
        return
    hasNoExoriGranCooldown = not cooldown.hasExoriGranCooldown(screenshot)
    if hasNoExoriGranCooldown:
        utils.core.press('F5')
        return
    hasNoExoriCooldown = not cooldown.hasExoriCooldown(screenshot)
    if hasNoExoriCooldown:
        utils.core.press('F3')
        return
    hasNoExoriMasCooldown = not cooldown.hasExoriMasCooldown(screenshot)
    if hasNoExoriMasCooldown:
        utils.core.press('F4')
        return


def shouldExecuteWaypoint(battleListCreatures, shouldIgnoreTargetAndGoToNextWaypoint):
    return battleListCreatures is not None and len(
        battleListCreatures) == 0 or shouldIgnoreTargetAndGoToNextWaypoint == True


def handleHungry(screenshot):
    if player.core.hasSpecialCondition(screenshot, 'hungry'):
        utils.core.press('F12')
    return


def handleHaste(screenshot):
    if not player.core.hasSpecialCondition(screenshot, 'haste'):
        utils.core.press('F9')
    return


def handleRing(screenshot):
    if not player.core.isEquipmentEquipped(screenshot, 'ring'):
        utils.core.press('F10')

    return


def handleNecklace(screenshot):
    if not player.core.isEquipmentEquipped(screenshot, 'necklace'):
        utils.core.press('F11')
    return


def main():
    global shouldIgnoreTargetAndGoToNextWaypoint
    optimal_thread_count = multiprocessing.cpu_count()
    threadPoolScheduler = ThreadPoolScheduler(optimal_thread_count)
    thirteenFps = 0.0667
    fpsObserver = rx.interval(thirteenFps)
    fpsWithScreenshot = fpsObserver.pipe(
        operators.map(handleWindow),
        operators.filter(lambda window: window is not None),
        operators.map(lambda window: utils.core.getScreenshot(window)),
    )
    coordinatesObserver = fpsWithScreenshot.pipe(
        operators.map(lambda screenshot: [screenshot, radar.core.getCoordinate(screenshot)]),
    )
    battlelistObserver = coordinatesObserver.pipe(
        operators.map(lambda result: [result[0], result[1], battleList.core.getCreatures(result[0])]),
    )
    hudCreaturesObserver = battlelistObserver.pipe(
        operators.map(
            lambda result: [result[0], result[1], result[2], hud.creatures.getCreatures(result[0], result[2])]),
    )

    cavebotObserver = hudCreaturesObserver.pipe(
        operators.filter(
            lambda result: result[2] is not None and len(
                result[3]) > 0 and shouldIgnoreTargetAndGoToNextWaypoint is False),
        operators.subscribe_on(threadPoolScheduler)
    )
    cavebotObserver.subscribe(
        lambda result: handleCavebot(result[0], result[1], result[2], result[3])
    )

    waypointObserver = hudCreaturesObserver.pipe(
        operators.filter(lambda result: shouldExecuteWaypoint(result[2], shouldIgnoreTargetAndGoToNextWaypoint)),
        operators.subscribe_on(threadPoolScheduler)
    )
    waypointObserver.subscribe(lambda result: handleWaypoints(result[0], result[1]))

    spellObserver = hudCreaturesObserver.pipe(
        operators.subscribe_on(threadPoolScheduler)
    )
    spellObserver.subscribe(lambda result: handleSpell(result[0], result[3]))

    healingObserver = fpsWithScreenshot.pipe(
        operators.map(lambda screenshot: (screenshot, player.core.getHealthPercentage(screenshot))),
        operators.map(lambda result: (result[1], player.core.getManaPercentage(result[0]))),
        operators.subscribe_on(threadPoolScheduler)
    )
    healingObserver.subscribe(lambda result: handleHealing(result[0], result[1]))

    hungryObserver = fpsWithScreenshot.pipe(
        operators.map(lambda screenshot: (screenshot, player.core.hasSpecialCondition(screenshot, 'hungry'))),
        operators.subscribe_on(threadPoolScheduler)
    )
    hungryObserver.subscribe(lambda result: handleHungry(result[0]))

    hasteObserver = fpsWithScreenshot.pipe(
        operators.map(lambda screenshot: (screenshot, player.core.hasSpecialCondition(screenshot, 'haste'))),
        operators.subscribe_on(threadPoolScheduler)
    )
    hasteObserver.subscribe(lambda result: handleHaste(result[0]))

    ringObserver = fpsWithScreenshot.pipe(
        operators.map(lambda screenshot: (screenshot, player.core.isEquipmentEquipped(screenshot, 'ring'))),
        operators.subscribe_on(threadPoolScheduler)
    )
    ringObserver.subscribe(lambda result: handleRing(result[0]))

    necklaceObserver = fpsWithScreenshot.pipe(
        operators.map(lambda screenshot: (screenshot, player.core.isEquipmentEquipped(screenshot, 'necklace'))),
        operators.subscribe_on(threadPoolScheduler)
    )
    necklaceObserver.subscribe(lambda result: handleNecklace(result[0]))


input("Press Enter key to exit...")

if __name__ == '__main__':
    main()
