from time import time
from chat import chat
from inventory import inventory
from player import player
from refill import refill
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
    window = getWindow()

    # Gets player Capacity
    screenshot = utils.getScreenshot(window)
    capValue = player.getCap(screenshot)
    print(f"Player capacity: {capValue}")

    # Selects the Server Log tab, reads the messages and gets all the lines with 'Loot of' in the text
    chat.selectServerLogTab(screenshot)
    screenshot = utils.getScreenshot(window)
    text = chat.readMessagesFromActiveChatTab(screenshot)
    lootText = chat.searchInActiveChatTab(text, ['Loot of'])
    print(lootText)

    # Starts conversation with NPC and buys items
    chat.sendMessage(screenshot, "hi")
    time.sleep(1)
    chat.sendMessage(screenshot, "trade")
    time.sleep(1)
    itemList = [('great-health-potion', 10), ('strong-mana-potion', 10)]
    refill.buyItems(window, itemList)

    # Opens the backpack, adjusts it and maps all the items inside with coordinates
    output = inventory.openMainBackpack(window)
    for i in range(len(output[1])):
        print(output[1][i])

if __name__ == '__main__':
    main()