import cv2 as cv
import numpy as np
import pyautogui
from PIL import ImageGrab


def grab_game_screen():
    if DEBUG:
        img = cv.imread('test_img/__screen.png')
        # cv.imshow("debug", img)
        # cv.waitKey(0)
        return img

    coin_screen_anchor = pyautogui.locateOnScreen('img/coins/coins-base.png', confidence=0.7)
    screen_box = (
        int(coin_screen_anchor.left - 57),
        int(coin_screen_anchor.top - 68),
        int(coin_screen_anchor.left - 57) + 1920,
        int(coin_screen_anchor.top - 68) + 1080
    )

    screen = np.array(ImageGrab.grab(bbox=(screen_box)))
    print(len(screen))
    rgb = cv.cvtColor(screen, cv.COLOR_BGR2RGB)

    if DEBUG:
        cv.imshow("debug", rgb)
        cv.waitKey(0)

    return rgb


def detect_coins():
    img = grab_game_screen()

    # Convert to HSV model to highlight green areas
    # H: 25 - 65 °
    # S: 50 - 100 %
    # V: 65 - 95 %
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, (25, 124, 165), (65, 255, 243))

    # Erosion / dilation to get rid of thin lines
    square = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, square, iterations=1)
    mask = cv.dilate(mask, square, iterations=1)

    # Find bounding boxes of each symbol
    bounding_boxes = []
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        bounding_boxes.append((x, y, w, h))
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv.imshow("debug", img)
    cv.waitKey(0)

    return None

    detected_digits = {}
    for digit in range(10):
        for box in _locate_all_no_overlap(f'img/coins/{str(digit)}.png', money_bounding_box, 0.95):
            detected_digits.update({int(box.left): str(digit)})

    money = ''
    for k, v in sorted(detected_digits.items()):
        money = money + v
    return int(money)


def test():
    # grab_game_screen()
    detect_coins()


if __name__ == '__main__':
    DEBUG = True
    test()
