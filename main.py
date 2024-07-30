from collections import deque

from calculator_engine import CalculatorEngine
from image_recognition_pag import detect_coins, detect_initial, detect_expected, detect_buttons


# DONE*: visual reading of buttons using pyautogui / pillow
#  * because as of now, reading buttons from screen is very unstable because of screen distortion while moving mouse

# TODO: interactive mode
#  - remember previous buttons
#  - read values from screen (money, initial, expected) using vision
#  - select solution from list of propositions and automatically remove used buttons
#  - ask user to type in new buttons we bought
#  -

# TODO: extra calculation, with or without +-10 joker button
# TODO: represent buttons as counts, sort solutions by buttons with highest count
# TODO: auto-disable one-digit mult/div optimizations if we generate 0 solutions

def _diff(a, b):
    """
    # list difference:
    # a = [1, 3, 3 ,7]
    # b = [3, 7]
    # diff(a, b) -> 1, 3
    """
    c = b[:]
    return [_ for _ in a if _ not in c or c.remove(_)]


def _breadth_first_search(initial_value, expected_value, button_list, money: int = 0):
    executed_instructions = 0
    current_depth = 0
    instructions_to_execute = deque()
    instructions_to_execute.append([])
    solutions = {}

    while instructions_to_execute and current_depth <= 5:
        # pick instruction to execute from queue
        current_instruction = instructions_to_execute.popleft()

        # print('ei', executed_instructions)
        # print('ite', instructions_to_execute)
        # print('ci', current_instruction)

        # calculate the result, if correct, add result to solutions and add instruction to list of already executed
        calculated_value = CalculatorEngine(initial_value, expected_value, current_instruction, money).run()
        if calculated_value == expected_value:
            solutions.update({', '.join(current_instruction): len(current_instruction)})
            # print({','.join(current_instruction): len(current_instruction)})
            current_depth = len(current_instruction)
        executed_instructions += 1

        # print('cv = ', calculated_value)
        # print('npm', next_possible_moves(current_instruction, diff(test_button_list, current_instruction)))

        # generate next instructions
        for move in CalculatorEngine().next_possible_moves(current_instruction,
                                                           _diff(button_list, current_instruction)):
            instructions_to_execute.append(current_instruction + [move])
            # print('ite', instructions_to_execute)

    # sort solutions by button count
    for k, v in sorted(solutions.items(), key=lambda kv: kv[1])[:10]:
        print(f'{v} moves: {k : <10}')
    print(f'calculated {executed_instructions} combinations')


def main():
    base_buttons = [
        '1', '1',
        '2', '2',
        '3', '3',
        '4', '4',
        '5', '5',
        '6', '6',
        '7', '7',
        '8', '8',
        '9', '9',
        '0', '0',
        '+', '+',
        '-', '-',
        'x', 'x',
        'div', 'div',
        # 'mod', 'mod',
        # 'x++', 'x++',
        # '+-10', '+-10',
        # 'reverse', 'reverse',
        # 'sqrt', 'sqrt',
        # '2-)4', '2-)4',
        # '5x', '5x',
        # 'x1', 'x1',
        # 'dollar', 'dollar',
        # 'x-)25', 'x-)25'
        # 'x^2', 'x^2',
    ]
    buttons = [
          #'1', #'1',  # '1',
          #'2', # '2',
        '3',    '3',
        # '4',  # '4',
        '5',  # '5',
        '6',    #'6',
        '7',  # '7',
        #'8',  # '8',
        '9',   '9',
        '0', '0',  # '0',
          #'+',  # '+',
        '-', #'-', #'-',
        #'x',  # 'x', #'x',
        # 'div', # 'div',
        # 'mod',  # 'mod',
        # 'x++',  # 'x++',
          #'+-10',  # '+-10',
         #'reverse',  # 'reverse',
          'sqrt',    'sqrt',# 'sqrt',
        '2-)4', '2-)4',
        # '5x',  # '5x',
        # 'x1',  # 'x1',
        #'dollar', 'dollar',
        # 'x-)25', # 'x-)25'
        # 'x^2', 'x^2',
        #'99',
    ]

    # boss fight: every click is double -> remove half of all buttons temporarily
    # buttons = set(buttons)

    # boss fight: can't see some labels -> remember previous round to use their button values

    money = detect_coins()
    print(f'money = {money} $')
    initial = detect_initial()
    print(f'initial = {initial}')
    expected = detect_expected()
    print(f'expected = {expected}')
    # buttons = detect_buttons()
    # print(f'buttons = {buttons}')

    _breadth_first_search(initial, expected, buttons, money)


def test():
    print(CalculatorEngine(72, 76, ['+', '4']).run(), 'expected 76')
    print(CalculatorEngine(72, 61, ['+-10']).run(), 'expected 62')

    print(CalculatorEngine(12, 21, ['reverse']).run(), 'expected 21')
    print(CalculatorEngine(123, 321, ['reverse']).run(), 'expected 321')
    print(CalculatorEngine(1, 1, ['reverse']).run(), 'expected 1')

    print(CalculatorEngine(25, 5, ['sqrt']).run(), 'expected 5')
    print(CalculatorEngine(35, 5, ['sqrt']).run(), 'expected 5')
    print(CalculatorEngine(26, 6, ['sqrt']).run(), 'expected 6')

    print(CalculatorEngine(1, 31, ['cut']).run(), 'expected 6')

    print(CalculatorEngine(10, 15, ['dollar'], 5).run(), 'expected 15')


if __name__ == '__main__':
    main()
    # test()
