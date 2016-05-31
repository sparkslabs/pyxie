#!/usr/bin/python

# mock functions/values to make prototyping/testing arduino stuff easier

def _trace(func, args):
    print func, args


HIGH="HIGH"
LOW="LOW"
OUTPUT="OUTPUT"

def digitalWrite(*args):         _trace("digitalWrite", args)
def delayMicroseconds(*args):    _trace("delayMicroseconds", args)
def pinMode(*args):              _trace("pinMode", args)
def analogRead(*args):           _trace("analogRead", args); return 0
def millis(*args):               _trace("millis", args); return 0

class Servo(object):
    def __init__(self):
        _trace("Servo.__init__", "")
        self.pin = None
    def writeMicroseconds(self, number):
        if self.pin != None:
            _trace("Servo.writeMicroseconds", [self.pin, number])
        else:
            _trace("Servo.writeMicroseconds", number)
    def attach(self, pin):
        _trace("Servo.attach", pin)
        self.pin = pin
