from microbit import *
import time
from random import randint


BOARD_MAX = 4
# game speed in seconds between steps
SNAKE_SPEED = 0.5


def turn_snake_left(orientation):
    return (orientation + 1) % 4


def turn_snake_right(orientation):
    orientation -= 1
    if orientation < 0:
        return 3
    return orientation


def move(snake, orientation, food):
    new_snake = []
    # move up
    if orientation == 0:
        if snake[0][1] == 0:
            return None, False
        new_head = (snake[0][0], snake[0][1] - 1)
    # move left
    elif orientation == 1:
        if snake[0][0] == 0:
            return None, False
        new_head = (snake[0][0] - 1, snake[0][1])
    # move down
    elif orientation == 2:
        if snake[0][1] == BOARD_MAX:
            return None, False
        new_head = (snake[0][0], snake[0][1] + 1)
    # move right
    else:
        if snake[0][0] == BOARD_MAX:
            return None, False
        new_head = (snake[0][0] + 1, snake[0][1])
    # check didn't crash to snake
    if new_head in snake:
        return None, False
    # move snake
    new_snake.append(new_head)
    if new_head == food:
        new_snake.extend(snake)
    else:
        new_snake.extend(snake[:-1])
    # draw updated snake
    for x, y in snake:
        display.set_pixel(x, y, 0)
    for x, y in new_snake:
        display.set_pixel(x, y, 9)
    eaten = len(new_snake) > len(snake)
    snake = new_snake
    return snake, eaten


def generate_randomly_food(snake):
    food_location = (randint(0, BOARD_MAX), randint(0, BOARD_MAX))
    while food_location in snake:
        food_location = (randint(0, BOARD_MAX), randint(0, BOARD_MAX))
    return food_location


# game reset loop
while True:
    display.scroll('GO')
    state = Image('00000:'
                  '00000:'
                  '00900:'
                  '00900:'
                  '00000')
    # 0 -> up, 1 -> left, 2 -> down, 3 -> right
    orientation = 0
    # counting score whnever there appears new food
    # so we have to start from -1
    score = -1
    snake = [(2, 2), (2, 3)]
    display.show(state)
    win = False
    food_eaten = True
    # game loop
    while True:
        past_orientation = orientation
        # food generation
        if food_eaten:
            food = generate_randomly_food(snake)
            food_eaten = False
            display.set_pixel(food[0], food[1], 4)
            score += 1
        # delay in order to make the game playble
        time.sleep(SNAKE_SPEED)
        # buton controling section
        if button_a.was_pressed():
            orientation = turn_snake_left(orientation)
        elif button_b.was_pressed():
            orientation = turn_snake_right(orientation)
        # movement
        snake, food_eaten = move(snake, orientation, food)
        if snake is None:
            break
        if len(snake) == 25:
            win = True
            break
    display.scroll('SCORE: ' + str(score))
    if win:
        display.scroll('VICTORY')
