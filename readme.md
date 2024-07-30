# `Calculate It` Solver

A simple solver to help in playing [Calculate It][1], a roguelike game that plays out on a calculator:

![Game screen][2]

Currently, it's a *Work In Progress*, as my solution using `pyautogui`/`pyscreeze` is struggling with performance,
I'm planning on moving into `opencv` and use a serious image processing / recognition approach.

If you're interested in running it, try and check out the code by yourself :) 

Example:

```text
calculate-it-solver\
 λ python main.py 
money = 0 $
initial = 14
expected = 110
3 moves: +, 9, 6   
4 moves: x, 8, -, 2
4 moves: +, 8, x, 5
5 moves: -, 3, +, 9, 9
5 moves: -, 2, +, 9, 8
5 moves: -, 1, +, 9, 7
5 moves: x, 6, +, 2, 6
5 moves: x, 7, +, 1, 2
5 moves: x, 4, +, 5, 4
5 moves: x, 3, +, 6, 8
calculated 37382 combinations

```

[1]: https://store.steampowered.com/app/3043740/Calculate_It/
[2]: test_img/__screen.png
