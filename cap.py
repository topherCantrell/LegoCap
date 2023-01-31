import time
import board
import pwmio
import busio
from adafruit_motor import motor
import random

import visuals

m2a = pwmio.PWMOut(board.GP10, frequency=50)
m2b = pwmio.PWMOut(board.GP11, frequency=50)
motor2 = motor.DCMotor(m2a, m2b)
motor2.throttle = None # Coast (low power)

i2c_alpha = busio.I2C(board.GP27,board.GP26)
i2c_grid  = busio.I2C(board.GP17,board.GP16)

i2c_grid.try_lock() # Leave it locked
i2c_grid.writeto(0x70, bytes([0b00100001]) ) # 0010_xxx1 Turn the oscillator on
i2c_grid.writeto(0x70, bytes([0b11101111]) ) # 1110_1111 Full brightness
i2c_grid.writeto(0x70, bytes([0b10000001]) ) # 1000_x001 Blinking off, display on
i2c_grid.writeto(0x70, bytes([0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])) # Blank

i2c_alpha.try_lock() # Leave it locked
i2c_alpha.writeto(0x70, bytes([0b00100001]) ) # 0010_xxx1 Turn the oscillator on
i2c_alpha.writeto(0x70, bytes([0b11101111]) ) # 1110_1111 Full brightness
i2c_alpha.writeto(0x70, bytes([0b10000001]) ) # 1000_x001 Blinking off, display on
i2c_alpha.writeto(0x70, bytes([0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])) # Blank

data = [
    [1,0,0,0,0,0,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,0,0,1,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,0,0,0,0,0,1],
]

def clear():
    for y in range(8):
        for x in range(8):
            data[y][x] = 0

def fizzle(num_dots):
    for i in range(num_dots):
        x = random.randint(0,7)
        y = random.randint(0,7)
        data[y][x] = 1

def fizzle_sleep(num_dots, cycles=8, time_wait=0.1):
    for i in range(cycles):
        clear()
        fizzle(num_dots)
        visuals.write_grid(i2c_grid, data)
        time.sleep(time_wait)

while True:
    #
    # FIZZ, "LEGO"
    #
    motor2.throttle=1
    fizzle_sleep(4)
    fizzle_sleep(4)
    visuals.show_message(i2c_alpha, '  3 ')
    fizzle_sleep(4)
    visuals.show_message(i2c_alpha, ' 2  ')
    fizzle_sleep(16)
    visuals.show_message(i2c_alpha, '1   ')
    fizzle_sleep(32)
    for i in range(5):
        visuals.show_message(i2c_alpha, 'LEGO')
        fizzle_sleep(50,cycles=2)
        visuals.show_message(i2c_alpha, '    ')
        fizzle_sleep(50,cycles=2)
    motor2.throttle=None

    #
    # HEART
    #
    for i in range(8):
        visuals.show_message(i2c_alpha, 'LEGO')
        visuals.draw_image(i2c_grid, visuals.IMG_HEART_SMALL)
        time.sleep(0.25)
        visuals.draw_image(i2c_grid, visuals.IMG_HEART_BIG)
        time.sleep(0.25)

    #
    # SMILE_BIG, "FLL 2023"
    #
    visuals.draw_image(i2c_grid,visuals.IMG_SMILE_BIG)
    msg = "   FLL 2023"
    for i in range(8):
        visuals.show_message(i2c_alpha, msg[i:i+4])
        time.sleep(0.5)

    #
    # ALIEN
    #
    motor2.throttle=-0.5
    visuals.show_message(i2c_alpha,"2023")
    for i in range(8):
        visuals.draw_image(i2c_grid, visuals.IMG_ALIEN1)
        time.sleep(0.5)
        visuals.draw_image(i2c_grid, visuals.IMG_ALIEN2)
        time.sleep(0.5)
    motor2.throttle=None

    #
    # SMILE, "ENER","GIZE"
    #
    visuals.draw_image(i2c_grid,visuals.IMG_SMILE)
    for i in range(4):
        visuals.show_message(i2c_alpha, "ENER")
        time.sleep(0.5)
        visuals.show_message(i2c_alpha, "GIZE")
        time.sleep(1)
        visuals.show_message(i2c_alpha, "    ")
        time.sleep(0.5)

    #
    # WIPE SQUARES
    #
    visuals.show_message(i2c_alpha,"FLL ")
    for i in range(len(visuals.IMG_SQUARE_WIPES)):
        visuals.draw_image(i2c_grid, visuals.IMG_SQUARE_WIPES[i])
        time.sleep(0.25)
    visuals.draw_image(i2c_grid, visuals.IMG_BLANK)

    #
    # SMILE_REV, "FUN "," FUN"
    #
    motor2.throttle=0.75
    visuals.draw_image(i2c_grid,visuals.IMG_SMILE_REV)
    for i in range(4):
        visuals.show_message(i2c_alpha, "FUN ")
        time.sleep(0.25)
        visuals.show_message(i2c_alpha, " FUN")
        time.sleep(0.25)    

    #
    # PLUS
    #
    visuals.show_message(i2c_alpha, "2023")
    for i in range(8):
        visuals.draw_image(i2c_grid, visuals.IMG_X)
        time.sleep(0.25)
        visuals.draw_image(i2c_grid, visuals.IMG_PLUS)
        time.sleep(0.25)
    motor2.throttle=None

    #
    # HOUR, "ROBO","TICS"
    visuals.draw_image(i2c_grid,visuals.IMG_HOUR)
    for i in range(4):
        visuals.show_message(i2c_alpha, "ROBO")
        time.sleep(0.5)
        visuals.show_message(i2c_alpha, "TICS")
        time.sleep(1)
        visuals.show_message(i2c_alpha, "    ")
        time.sleep(0.5)

    #
    # SQUARES
    #
    motor2.throttle=-0.75
    rev=random.randint(0,1)
    visuals.show_message(i2c_alpha, "FLL ")
    for i in range(8):
        visuals.draw_image(i2c_grid, visuals.IMG_SQUARES1,rev)
        time.sleep(0.25)
        visuals.draw_image(i2c_grid, visuals.IMG_SQUARES2,rev)
        time.sleep(0.25)
    motor2.throttle=None

    #
    # SKULL, "ENER","GIZE"
    #
    visuals.draw_image(i2c_grid,visuals.IMG_SKULL,True)
    for i in range(4):
        visuals.show_message(i2c_alpha, "ENER")
        time.sleep(0.5)
        visuals.show_message(i2c_alpha, "GIZE")
        time.sleep(1)
        visuals.show_message(i2c_alpha, "    ")
        time.sleep(0.5)