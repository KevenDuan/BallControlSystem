# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = board.I2C()  # uses board.SCL and board.SDA
pca = PCA9685(i2c)
pca.frequency = 50
servo7 = servo.Servo(pca.channels[7])
servo8 = servo.Servo(pca.channels[8])

servo7.angle = 80
servo8.angle = 73

pca.deinit()

