# Basic movement script for PCA9685 control of my RC car
# Author: Matthew Hough
# Controls:
# - Forward = Up arrow
# - Back = Down arrow
# - Left = Left arrow
# - Right = Right arrow
# - Stop = Spacebar



import Adafruit_PCA9685
import time
import curses

MAX_L = 220
MAX_R = 420
MAX_UP = 618
MAX_DOWN = 183
STOP_RANGE = range(364,382+1)

# veer error - my car veers left due to a bad wheel
VEER_ERR = 10
MID = 320 + VEER_ERR
STOP = 373
FORWARD = 386
BACKWARD = 359

# Change in pos/accel per move
DELTA_POS = 30
DELTA_ACCEL = 2

# Motor channels
STEER = 0
MOVE = 1

# Should be stopped initially
pos = MID
accel = STOP

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60) # supposed to be good for servos

# Get screen and turn off input
# echoing, respond to key presses
# immediately, and map arrow keys
# to special values
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

screen.addstr(0,0,f'MOTOR0: {pos}\nMOTOR1: {accel}')
pwm.set_pwm(STEER,0,pos)
pwm.set_pwm(MOVE,0,accel)
while True:
    # TODO: If haven't got a signal in 1 sec or so, go to stop/mid position. - SAFETY
    char = screen.getch()
    if char == ord(' '):
        accel = STOP
    elif char == curses.KEY_LEFT:
        if pos >= (MAX_L+DELTA_POS):
            pos -= DELTA_POS
    elif char == curses.KEY_RIGHT:
        if pos <= (MAX_R-DELTA_POS):
            pos += DELTA_POS
    elif char == curses.KEY_UP:
        if accel == STOP:
            accel = FORWARD
        elif accel <= (MAX_UP-DELTA_ACCEL):
            if accel in STOP_RANGE:
                accel = STOP
            else:
                accel += DELTA_ACCEL
    elif char == curses.KEY_DOWN:
        if accel == STOP:
            accel = BACKWARD
        elif accel >= (MAX_DOWN+DELTA_ACCEL):
            if accel in STOP_RANGE:
                accel = STOP
            else:
                accel -= DELTA_ACCEL
    elif char == ord('q'):
        pos = MID
        accel = STOP

        curses.endwin()
        break

    # Send changes to motors
    screen.addstr(0,0,f'MOTOR0: {pos}\nMOTOR1: {accel}')
    pwm.set_pwm(STEER,0,pos)
    pwm.set_pwm(MOVE,0,accel)
