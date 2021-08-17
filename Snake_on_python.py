# -*- coding: utf-8 -*-
# Created on 20th,Apr.2021
# Modified on 22nd,Apr.2021
# @author: I-am-Future

import turtle as tu
from random import randint
import time


# GLOBAL_VARIABLES_list_here:

# g_status_pen, to print status bar
g_status_pen = tu.Turtle()
g_status_pen.up()
g_status_pen.hideturtle()
# g_food_pen, to print food items
g_food_pen = tu.Turtle()
g_food_pen.up()
g_food_pen.hideturtle()

g_motion = -1  # -1:init, 0:up, 1:down, 2:left, 3:right
g_isPaused = True   # True: Pause, False: Playing
g_contact = 0   # to store the contact times
g_starttime = -1   # to store the starting time, origin is -1
g_monster_speed = 250   # the speed of monster
g_snake_speed = 250   # the speed of snake
g_snake_length = 5   # original length
g_snakebody_index = []   # to store the index of each snake body
g_snakebody_pos = []   # to store the position of each snake body
g_food_list = []   # to store the position of each food item
prompt_init = 'Welcome to Future\'s Snake!\n' + \
    'You are going to use 4 arrow keys to move the snake\n' + \
    'around the screen, trying to sonsume all the food item\n' +\
    'before the monster catches you.\n\n' + \
    'Click anywhere on the screen to start the game!!!'


def initialization_ui():
    '''initialize the whole screen, with a screen(global) and two areas.'''
    global g_screen, g_prompts_pen
    # whole screen here
    g_screen = tu.Screen()
    g_screen.setup(660, 740)
    g_screen.title('Snake by Lai WEI')
    g_screen.tracer(0)
    # main game area here
    area_down = tu.Turtle('square')
    area_down.penup()
    area_down.goto(0, -40)
    area_down.color('black', '')
    area_down.shapesize(25, 25)
    # head bar here
    area_up = tu.Turtle('square')
    area_up.penup()
    area_up.goto(0, 250)
    area_up.color('black', '')
    area_up.shapesize(4, 25)
    # g_prompts_pen
    g_prompts_pen = tu.Turtle()
    g_prompts_pen.up()
    g_prompts_pen.hideturtle()
    g_prompts_pen.goto(-220, 90)
    g_prompts_pen.write(prompt_init, font=('Arial', 12, 'normal'))
    g_screen.update()


def initialization_objects():
    '''initialize the snake(global), and the monster(global)'''
    global g_snake, g_monster, g_food_pen
    # generate snake
    g_snake = tu.Turtle('square')
    g_snake.color('red')
    g_snake.penup()
    g_snake.goto(0, -40)
    # generate monster
    g_monster = tu.Turtle('square')
    g_monster.color('purple')
    g_monster.penup()
    monster_x = randint(-11, 9) * 20 + randint(0,19)
    monster_y = randint(-12, 8) * 20 + randint(0,19)
    while abs(monster_x) + abs(monster_y+40) < 240:
        monster_x = randint(-11, 9) * 20 + randint(0,19)
        monster_y = randint(-12, 8) * 20 + randint(0,19)
    g_monster.goto(monster_x, monster_y)
    # generate food
    for i in range(1, 10):
        food_x = randint(-10, 10) * 20
        food_y = randint(-10, 10) * 20
        while abs(food_x) + abs(food_y) < 160 or \
                ((food_x, food_y) in g_food_list):
            food_x = randint(-10, 10) * 20
            food_y = randint(-10, 10) * 20
        g_food_list.append((food_x, food_y))
    g_screen.update()


def display_status():
    '''display the status of the game on the top of the UI'''
    global g_status_pen
    status_list = ['Up', 'Down', 'Left', 'Right']
    g_status_pen.clear()
    g_status_pen.goto(-220, 240)
    g_status_pen.write('Contact:%d' % g_contact, font=('Arial', 14, 'normal'))
    g_status_pen.goto(-50, 240)
    if g_starttime == -1:    # before starting
        g_status_pen.write('Time:%d' % (0), font=('Arial', 14, 'normal'))
    else:    # game starts
        g_status_pen.write('Time:%d' % (
            time.time()-g_starttime), font=('Arial', 14, 'normal'))
    g_status_pen.goto(70, 240)
    if g_isPaused:    # paused, print Paused
        g_status_pen.write('Motion:%s' % ('Paused'),
                           font=('Arial', 14, 'normal'))
    else:    # print current heading
        g_status_pen.write('Motion:%s' %
                        status_list[g_motion], font=('Arial', 14, 'normal'))
    g_screen.update()


def pause():
    '''bind for the space'''
    global g_isPaused
    g_isPaused = not g_isPaused


def up():
    '''bind for the Up'''
    global g_motion, g_isPaused
    g_motion = 0
    g_isPaused = False


def down():
    '''bind for the Down'''
    global g_motion, g_isPaused
    g_motion = 1
    g_isPaused = False


def left():
    '''bind for the Left'''
    global g_motion, g_isPaused
    g_motion = 2
    g_isPaused = False


def right():
    '''bind for the Right'''
    global g_motion, g_isPaused
    g_motion = 3
    g_isPaused = False


def check_win():
    '''check if player win/lose'''
    global g_prompts_pen
    if g_food_list == [(-1, -1)]*9:    # the player wins
        g_prompts_pen.goto(g_snake.xcor()-20,g_snake.ycor()+10)
        g_prompts_pen.color('red')
        g_prompts_pen.write('Winner!!!', font=('Arial', 12, 'normal'))
        return 0  # the player wins
    elif g_monster.distance(g_snake) < 20:     # the player loses
        g_prompts_pen.goto(g_monster.xcor()-20,g_monster.ycor()+10)
        g_prompts_pen.color('purple')
        g_prompts_pen.write('Game over!!!', font=('Arial', 12, 'normal'))
        return 1  # the player loses


def check_food():
    '''check if the snake is on the food position'''
    global g_food_list, g_snake_length
    if g_snake.position() in g_food_list:    
        g_snake_length += (g_food_list.index(g_snake.position())+1)
        g_food_list[g_food_list.index(g_snake.position())] = (-1, -1)
        update_food()


def check_contact():
    '''check and count if it is contacted'''
    global g_contact
    if any([g_monster.distance(x,y)<20 for (x,y) in g_snakebody_pos]):
        g_contact += 1


def monster_chase():
    '''return the best next step for monster to chase
        return value: next (x,y) position
    '''
    snake_x, snake_y = g_snake.position()
    monster_x, monster_y = g_monster.position()
    if abs(snake_x-monster_x) > abs(snake_y-monster_y):
        if snake_x > monster_x:
            return (monster_x+20, monster_y)
        else:
            return (monster_x-20, monster_y)
    else:
        if snake_y > monster_y:
            return (monster_x, monster_y+20)
        else:
            return (monster_x, monster_y-20)


def update_food():
    '''update the food display'''
    global g_food_pen
    g_food_pen.clear()
    for i in range(9):
        pos = g_food_list[i]
        if pos != (-1, -1):
            g_food_pen.goto(pos[0]-3, pos[1]-10)
            g_food_pen.write(i+1, font=('Arial', 12, 'normal'))
    g_screen.update()


def update_snake():
    '''update the snake's movement'''
    global g_snakebody_index, g_snakebody_pos
    movements = {0: (0, 20), 1: (0, -20), 2: (-20, 0), 3: (20, 0)}
    check_win()
    if check_win() is None:
        if ((not g_isPaused) and
                (not ((g_snake.position()[0] == -240 and g_motion == 2) or
                      (g_snake.position()[0] == 240 and g_motion == 3) or
                      (g_snake.position()[1] == 200 and g_motion == 0) or
                      (g_snake.position()[1] == -280 and g_motion == 1)))):
            g_snake.color('black', 'blue')
            g_snakebody_index.append(g_snake.stamp())
            g_snakebody_pos.append(g_snake.position())
            new_snake_x = g_snake.position()[0] + movements[g_motion][0]
            new_snake_y = g_snake.position()[1] + movements[g_motion][1]
            g_snake.goto(new_snake_x, new_snake_y)
            g_snake.color('red')
            check_food()
            if len(g_snakebody_index) > g_snake_length:
                g_snake.clearstamp(g_snakebody_index.pop(0))
                g_snakebody_pos.pop(0)
                g_screen.ontimer(update_snake, g_snake_speed)
            else:  # snake is not extending
                g_screen.ontimer(update_snake, int(1.25*g_snake_speed))
        else:
            g_screen.ontimer(update_snake, g_snake_speed)
    g_screen.update()


def update_monster():
    '''update the monster's next step on the screen'''
    global g_monster_speed
    check_contact()
    display_status()
    if check_win() is None:
        g_monster.goto(monster_chase())
        g_screen.ontimer(update_monster, randint(
            0.9*g_monster_speed, 1.8*g_monster_speed))
        g_screen.update()


def main_game(p_x, p_y):
    '''click the screen and start the game in this function'''
    global g_starttime
    print('game on!!!')
    g_prompts_pen.clear()
    g_starttime = time.time()
    g_screen.onclick(None)    # remove the click binding
    g_screen.onkeypress(pause, 'space')
    g_screen.onkeypress(up, 'Up')
    g_screen.onkeypress(down, 'Down')
    g_screen.onkeypress(left, 'Left')
    g_screen.onkeypress(right, 'Right')
    g_screen.ontimer(update_monster, g_monster_speed)
    g_screen.ontimer(update_snake, g_snake_speed)
    update_food()


initialization_ui()  # initialize the game UI
initialization_objects()  # initialize the game objects
display_status()  # display the status
g_screen.onclick(main_game)  # toggle to start the game
tu.listen()
tu.done()
