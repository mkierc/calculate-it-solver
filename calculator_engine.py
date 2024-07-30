import math
import re


class CalculatorEngine(object):
    num_ops = ['+', '-', 'x', 'div', 'mod']
    simple_ops = ['x++', '+-10', 'reverse', 'sqrt', '2-)4', '5x', 'x1', 'dollar', 'x-)25', 'x^2']

    def next_possible_moves(self, current_state: list[str], button_list: list[str]):

        next_possible_moves = []

        # empty stack or simple op -> use num_ops or simple_ops
        if not current_state or current_state[-1] in self.simple_ops:
            for move in button_list:
                if move in self.num_ops or move in self.simple_ops:
                    next_possible_moves.append(move)

        # last move was a number operator -> requires a digit
        elif current_state[-1] in self.num_ops:
            for move in button_list:
                if move.isdigit():
                    next_possible_moves.append(move)

        # last move was a digit
        elif current_state[-1].isdigit():
            # last two were both digits -> just ops, limit number of digits to two
            if current_state[-2].isdigit():
                for move in button_list:
                    if move in self.num_ops or move in self.simple_ops:
                        next_possible_moves.append(move)
            # limit multiplication and division to one digit only
            elif current_state[-2] in ['x', 'div']:
                for move in button_list:
                    if move in self.num_ops or move in self.simple_ops:
                        next_possible_moves.append(move)
            else:
                next_possible_moves.extend(button_list)

        # not possible
        else:
            raise NotImplementedError

        # pruning:
        next_possible_moves = list(set(next_possible_moves))

        if current_state:
            if current_state[-1] in ['+', '-', 'mod']:
                if '0' in next_possible_moves:
                    next_possible_moves.remove('0')
            elif current_state[-1] in ['x', 'div']:
                if '1' in next_possible_moves:
                    next_possible_moves.remove('1')
            # use 'x-)25' only in empty states, otherwise it's wasted
            if 'x-)25' in next_possible_moves:
                next_possible_moves.remove('x-)25')

        return next_possible_moves

    def prepare_instruction_list(self, instruction_list):
        # concatenate consecutive numbers
        result = []
        num = ''

        for char in instruction_list:
            if char.isdigit():
                num += char
            else:
                if num:
                    result.append(num)
                    num = ''
                result.append(char)

        if num:
            result.append(num)

        return result

    def __init__(self, initial_value: int = 0, expected_value: int = 0, instruction_list: list = [], money: int = 0):
        self.current_value = initial_value
        self.expected_value = expected_value
        self.money = money
        self.instruction_list = self.prepare_instruction_list(instruction_list)
        # set pointer at first instruction
        self.pointer = 0

    def execute(self, instruction):
        # num ops, offset pointer by 2
        if instruction == '+':
            self.current_value = self.current_value + int(self.instruction_list[self.pointer + 1])
            self.pointer = self.pointer + 2
        elif instruction == '-':
            self.current_value = self.current_value - int(self.instruction_list[self.pointer + 1])
            self.pointer = self.pointer + 2
        elif instruction == 'x':
            self.current_value = self.current_value * int(self.instruction_list[self.pointer + 1])
            self.pointer = self.pointer + 2
        elif instruction == 'div':
            if int(self.instruction_list[self.pointer + 1]) == 0:
                raise IndexError
            self.current_value = self.current_value // int(self.instruction_list[self.pointer + 1])
            self.pointer = self.pointer + 2
        elif instruction == 'mod':
            self.current_value = self.current_value % int(self.instruction_list[self.pointer + 1])
            self.pointer = self.pointer + 2
        # simple ops, offset pointer by 1
        elif instruction == 'x++':
            self.current_value = self.current_value + 1
            self.pointer = self.pointer + 1
        elif instruction == '+-10':
            diff = abs(self.expected_value - self.current_value)
            if diff < 10:
                if self.expected_value < self.current_value:
                    self.current_value = self.current_value - diff
                elif self.expected_value > self.current_value:
                    self.current_value = self.current_value + diff
            else:
                if self.expected_value < self.current_value:
                    self.current_value = self.current_value - 10
                elif self.expected_value > self.current_value:
                    self.current_value = self.current_value + 10

            self.pointer = self.pointer + 1
        elif instruction == 'reverse':
            # # value is capped at 0, no need to check
            # if self.current_value < 0:
            #     self.current_value = -int(str(abs(self.current_value))[::-1])
            # else:
            #     self.current_value = int(str(self.current_value)[::-1])
            self.current_value = int(str(self.current_value)[::-1])
            self.pointer = self.pointer + 1
        elif instruction == 'sqrt':
            if self.current_value > 0:
                self.current_value = round(math.sqrt(self.current_value))
            self.pointer = self.pointer + 1
        elif instruction == '2-)4':
            if '2' not in str(self.current_value):
                raise IndexError
            self.current_value = int(str(self.current_value).replace('2', '4'))
            self.pointer = self.pointer + 1
        elif instruction == '5x':
            self.current_value = int(f'5{self.current_value}')
            self.pointer = self.pointer + 1
        elif instruction == 'x1':
            self.current_value = int(f'{self.current_value}1')
            self.pointer = self.pointer + 1
        elif instruction == 'dollar':
            if self.money == 0:
                raise IndexError
            self.current_value = self.current_value + self.money
            self.pointer = self.pointer + 1
        elif instruction == 'x-)25':
            self.current_value = 25
            self.pointer = self.pointer + 1
        elif instruction == 'x^2':
            self.current_value = self.current_value * self.current_value
            self.pointer = self.pointer + 1
        else:
            print(self.instruction_list)
            raise NotImplementedError

        if self.current_value < 0:
            self.current_value = 0

    def run(self):
        # if the instruction ends in a number operation without a number, instruction is invalid
        if self.instruction_list and self.instruction_list[-1] in self.num_ops:
            return None

        while self.pointer < len(self.instruction_list):
            try:
                self.execute(self.instruction_list[self.pointer])
            except IndexError:
                # instruction does not make sense
                return None

        return self.current_value
