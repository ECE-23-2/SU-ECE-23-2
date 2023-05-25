# import complex math module
import cmath
import math

from localizationFunctions import *
# #############################
# x_1, y_1 = -6, 2  # Left
# x_2, y_2 = -6, -2  # Right
# x_3, y_3 = 0, 0  # Front
#
# # From left to right order of the landing gears first, second third
# first_r = math.sqrt(18)
# second_r = math.sqrt(10)
# third_r = math.sqrt(34)
#
# first_a = 315  # in degrees right now
# second_a = 71.5651
# third_a = 30.9638

#############################
# x_1, y_1 = -6, 2
# x_2, y_2 = -6, -2
# x_3, y_3 = 0, 0
#
# # From left to right order of the landing gears first, second third
# first_r = math.sqrt(34)
# second_r = math.sqrt(10)
# third_r = math.sqrt(18)
#
# first_a = 329.036  # in degrees right now
# second_a = 288.435
# third_a = 45

############################
# # Top view
# x_1, y_1 = 2390, -333 # Left
# x_2, y_2 = 2390, 333 # Right
# x_3, y_3 = 720, 0 # Front
#
# # From left to right order of the landing gears first, second third
# first_r = 2322
# second_r = 2578
# third_r = 1126
#
# first_a = 10.9435  # in degrees right now
# second_a = 25.5539
# third_a = 52.7694

############################

# Top view
x_1, y_1 = 2390, -333 # Left
x_2, y_2 = 2390, 333 # Right
x_3, y_3 = 720, 0 # Front

# From left to right order of the landing gears first, second third
first_r = 2322
second_r = 2578
third_r = 1126

first_a = 10.9435  # in degrees right now
second_a = 25.5539
third_a = 52.7694

x, y = finalFunction(first_r, first_a, second_r, second_a, third_r, third_a, x_1, y_1, x_2, y_2, x_3, y_3)

































