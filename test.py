from time import time
from chat import chat
from utils import utils
import pygetwindow as gw


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


def main():
    loop_time = time()
    window = getWindow()
    while True:
        screenshot = utils.getScreenshot(window)
        #print(chat.selectServerLogTab(screenshot))
        text = chat.readMessagesFromActiveChatTab(screenshot)
        lootText = chat.searchInActiveChatTab(text, ['Loot of'])
        break
        # timef = (time() - loop_time)
        # timef = timef if timef else 1
        # fps = 1 / timef
        # print('FPS {}'.format(fps))
        # loop_time = time()

if __name__ == '__main__':
    main()
