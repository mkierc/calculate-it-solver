import pyautogui
import pyscreeze

# TODO: this is the first, naive approach using just pyautogui w/ pyscreeze and it's locateAllOnScreen() method
#  very inconsistent because of parts of the screen moving along with the mouse, and very slow having to do
#  a sweep search over large areas of the screen - but I'm leaving the code to serve as a basis to work out
#  a better way, using the powers of OpenCV image processing methods


def _locate_all_no_overlap(image, region, confidence, overlap=10, grayscale=False):
    distance = pow(overlap, 2)
    found = []
    try:
        for image in pyautogui.locateAllOnScreen(image, grayscale=grayscale, region=region, confidence=confidence):
            if all(map(lambda x: pow(image.left - x.left, 2) + pow(image.top - x.top, 2) > distance, found)):
                found.append(image)
    except pyscreeze.ImageNotFoundException:
        return []
    return found


def _expand_button_box(box):
    x, y, w, h = box.left, box.top, box.width, box.height

    center_x = int(x + (w // 2))
    center_y = int(y + (h // 2))

    new_x = center_x + 20
    new_y = center_y - 50
    new_w = 25
    new_h = 50

    return new_x, new_y, new_w, new_h


def detect_coins():
    coin_screen_anchor = pyautogui.locateOnScreen('img/coins/coins-base.png', confidence=0.7)
    money_bounding_box = [
        coin_screen_anchor.left + coin_screen_anchor.width,
        coin_screen_anchor.top - 25,
        120,
        90
    ]

    detected_digits = {}
    for digit in range(10):
        for box in _locate_all_no_overlap(f'img/coins/{str(digit)}.png', money_bounding_box, 0.95):
            detected_digits.update({int(box.left): str(digit)})

    money = ''
    for k, v in sorted(detected_digits.items()):
        money = money + v
    return int(money)


def detect_initial():
    coin_screen_anchor = pyautogui.locateOnScreen('img/coins/coins-base.png', confidence=0.9)
    initial_value_bounding_box = [
        coin_screen_anchor.left + 1500,
        coin_screen_anchor.top + 680,
        350,
        200
    ]

    detected_digits = {}
    for digit in range(10):
        for box in _locate_all_no_overlap(f'img/initial/{str(digit)}.png', initial_value_bounding_box, 0.95):
            detected_digits.update({int(box.left): str(digit)})

    initial = ''
    for k, v in sorted(detected_digits.items()):
        initial = initial + v
    return int(initial)


def detect_expected():
    coin_screen_anchor = pyautogui.locateOnScreen('img/coins/coins-base.png', confidence=0.9)
    expected_value_bounding_box = [
        coin_screen_anchor.left + 1700,
        coin_screen_anchor.top + 560,
        150,
        100
    ]

    detected_digits = {}
    for digit in range(10):
        for box in _locate_all_no_overlap(f'img/expected/{str(digit)}.png', expected_value_bounding_box, 0.95):
            detected_digits.update({int(box.left): str(digit)})

    initial = ''
    for k, v in sorted(detected_digits.items()):
        initial = initial + v
    return int(initial)


def detect_buttons():
    buttons = [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '0',
        '+',
        '-',
        'x',
        'div',
        # 'mod',
        'x++',
        # '+-10',
        'reverse',
        # 'sqrt',
        # '2-)4',
        '5x',
        'x1',
        'dollar',
        'x-)25',
        # 'x^2',
    ]

    use_count = [
        0, 1, 2, 3, 4
    ]

    coin_screen_anchor = pyautogui.locateOnScreen('img/coins/coins-base.png', confidence=0.9)
    buttons_value_bounding_box = (
        int(coin_screen_anchor.left - 50),
        int(coin_screen_anchor.top + 400),
        1400,
        500
    )

    # # old approach: find all button positions by empty button image, then for each button find the type and value
    # detected_button_locations = []
    #
    # located = locate_all_no_overlap(f'img/buttons/generic_button.png',
    #                                 buttons_value_bounding_box, 0.6, grayscale=True, overlap=100)
    #
    # for n, box in enumerate(located):
    #     a, b, c, d = box.left, box.top, box.width, box.height
    #     print(n, (int(a), int(b), c, d))
    #     detected_button_locations.append(box)
    #     pyscreeze.screenshot(imageFilename=f'{n}.png', region=(int(a), int(b), c, d))

    # # new approach:
    # - find bounding box of only the button symbol,
    # - calculate middle point,
    # - calculate button bounding box
    # - find its value

    # # DEBUG - field where all calculator buttons reside
    # pyscreeze.screenshot(imageFilename=f'test_img/field.png', region=buttons_value_bounding_box)

    detected_buttons = {}
    for button in buttons:
        for box in _locate_all_no_overlap(f'img/buttons/{button}.png', buttons_value_bounding_box, 0.85, overlap=30, grayscale=True):
            expanded = _expand_button_box(box)
            values = []
            for value in use_count:
                try:
                    pyscreeze.screenshot(imageFilename=f'test_img/{button}.png', region=(int(box.left), int(box.top), box.width, box.height))
                    pyscreeze.screenshot(imageFilename=f'test_img/{button}-value.png', region=expanded)
                    if pyautogui.locateOnScreen(image=f'img/buttons/values/{value}.png', grayscale=True,
                                                region=expanded, confidence=0.9):
                        values.append(value)
                except pyautogui.ImageNotFoundException:
                    pass

            try:
                detected_buttons.update({button: values[0]})
            except IndexError:
                pass
                # print(f"DEBUG: missing value for {button}")

    button_list = []

    for button, value in sorted(detected_buttons.items(), key=lambda kv: kv[1], reverse=True):
        for n in range(value):
            button_list.append(button)

    return button_list


def test():
    # print(f'money = {detect_coins()} $')
    # print(f'initial = {detect_initial()}')
    # print(f'expected = {detect_expected()}')
    # print(f'buttons = {detect_buttons()}')

    print(f'screen = {detect_game_screen()}')


if __name__ == '__main__':
    test()
