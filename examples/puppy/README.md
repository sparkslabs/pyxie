Puppy
-----

The Dagu playful puppy is a simple, fun, dog shaped robot.

This directory will contain example Pyxie code for programming this device.

Current status is that the TARGET versions of this code do not work yet.

HOWEVER as of October 2016, the minimal version - which allows the robot
to read it's sensors and move around, DOES work.

This is a huge step forward, since we have the start of making autonomous
robots using Pyxie.

puppy/target
------------

The current status is that this TAREGT code does not yet compile, however,
it is a first cut of something that *could* be compiled by Pyxie for a real
world device.

This is a device that is powered by an Atmel 8A arduino.

Files:

  - nofunctions_playfulpuppy.pyxie - A pyxie version of the code with no
    - PARSES correctly by Pyxie

  - nofunctions_playfulpuppy.py - A python version with simple mock stubs
    for the arduino functions.  (The stubs are the only change)
    - Runs on CPython as intended

