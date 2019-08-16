import Adafruit_PCA9685
import curses

MAX_L = 220
MAX_R = 420
# veer error - my car veers left due to a bad wheel
VEER_ERR = 10
MID = 320 + VEER_ERR

# Change in pos/accel per move
DELTA_POS = 10
DELTA_ACCEL = 10

# Motor channels
STEER = 0
MOVE = 1

# TODO: add accel/decel values

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

# Should be stopped initially
pos = MID
accel = 0 # STOP

while True:
    # TODO: If haven't got a signal in 1 sec or so, go to stop/mid position. - SAFETY
    char = screen.getch()
    if char == curses.KEY_LEFT:
        if pos >= (MAX_L+DELTA_POS):
            screen.addstr(0,0,f'TRUE LEFT')
            pos = MID - DELTA_POS
    elif char == curses.KEY_RIGHT:
        if pos <= (MAX_R-DELTA_POS):
            screen.addstr(0,0,f'TRUE RIGHT')
            pos = MID + DELTA_POS
    elif char == ord('q'):
        pos = MID
        # accel = STOP

        #  curses.nocbreak()
        #  screen.keypad(False)
        #  curses.echo()
        curses.endwin()
        break

    # Send changes to motors
    screen.addstr(0,0,f'MOTOR0: {pos}\nMOTOR1: {accel}')
    pwm.set_pwm(STEER,0,pos)
    #  pwm.set_pwm(MOVE,0,accel)
