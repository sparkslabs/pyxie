#!/usr/bin/python

from arduino import *

myservo = Servo()
pos = 0
pin=11

myservo.attach(pin)
