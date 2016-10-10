## Arduino Profile

Pyxie supports the concept of profiles - that is compilation environments.
The arduino profile triggers the creation of code suitable for compilation
with the arduino toolchain that can run on arduino devices.

### Is this Useful?

Yes, this should be. This is definitely sufficient for building little robots
that are made of microcontrollers, servos, sensors and can report data via
the serial port. That in itself covers an awful lot of use-cases!

Bear in mind though that pyxie is pre-alpha, and error messages are at best
cryptic, and also that the language is VERY far from being anywhere near
complete.

### Initialise your variables.

In order to simplify identification of types, **always initialise all variables** before you use them.
We could do better than this, but at this stage, it makes a big difference.
In particular, it enables alot of what makes this useful.

## Usage

You write your python program as normal - except you can use the functions that
someone writing an arduino program uses. For example, the blink arduino program
looks like this in python:

    led = 13

    pinMode(led, OUTPUT)

    while True:
        digitalWrite(led, HIGH)
        delay(1000)
        digitalWrite(led, LOW)
        delay(1000)

To compile this, assuming you've installed pyxie - you do this:

    ./bin/pyxie --profile arduino compile arduino-blink.pyxie

This compiles the code, and creates a **`build-TIMESTAMP directory`** . If you
want to upload this to your device, change into that directory, and do
a **`make upload`** .

For example

    ./bin/pyxie --profile arduino compile arduino-blink.pyxie
    cd build-1234567890
    make upload

If you have an Arduino Leonardo - or similar/compatible device - attached
to **`/dev/ACM0`** , then this will upload the code onto your device.

### Compiling for YOUR arduino device

The approach in the section above worse fine. However, you might not have
an Arduino Leonardo (or something similar Atmega 32U4 based). Or even if
you do, it might show up on a different port from **`/dev/ACM0`** - it might
show up as **`/dev/ACM1`** for example.

To control the board you're building for, and the port your board is
connected to, you can create a **`program-name.Makefile.in`** file.

So for example, you have a program called **`arduino-blink.pyxie`** that
looks like this:

    led = 13

    pinMode(led, OUTPUT)

    while True:
        digitalWrite(led, HIGH)
        delay(1000)
        digitalWrite(led, LOW)
        delay(1000)

... and you have an atmega8 based device (eg a Dagu Mini) on port **`/dev/ACM1`** .
You create a file called **`arduino-blink.Makefile`** .in with the following
contents:

    BOARD_TAG    = atmega8
    ARDUINO_PORT = /dev/ttyACM1

You can then build your program and upload it to the device as follows:

    ./bin/pyxie --profile arduino compile arduino-blink.pyxie
    cd build-1234567890
    make upload

This uses the contents of your **`program-name.Makefile.in`** file to override the defaults
that would otherwise be used.

## Examples

There are a handful of examples in the **examples/** directory.

* [arduino][ARDUINOEXAMPLE] - basic example that blinks a light on/off
* [servo][SERVOEXAMPLE] - Example that shows how to use servo motors
* [analog][ANALOGEXAMPLE] - Example that shows how to use analog sensors and the serial port
* [puppy][PUPPYEXAMPLE] - Sample code for controlling the Dagu Playful puppy. (A quaduped
  robot with 10 servos and an an IR sensor based "head")

Links above take you to github locations for the code.

## Status

### Functions/etc available

Function/functionality specifically checked:

* `digitalWrite`
* `analogRead` , `analogWrite`
* `constrain` , `map`
* `delay` , `millis` , `delayMicroseconds`
* `random` , `randomSeed`
* `Serial.begin` , `Serial.print` , `Serial.println`

Servo functionality tested:

* `#include <Servo.h>` -- (ab)uses fact that "#" is a comment in python
* `Servo()` -- works as expected.
* `servo.attach(pin)` - works as expected.
* `servo.write(pos)` - works as expected.
* `servo.writeMicroseconds` - works as expected.

Variables/Constants made available:

* `A0` , `A1` , `A2` , `A3` , `A4` , `A5` , `A6` , `A7`
* `HIGH` , `LOW`
* `INPUT` , `OUTPUT`

### Other Arduino Variables?

`IN`/`OUT`/etc need to be predefined to work. The same would go for many other
Arduino variables that are defined in the library. I will have missed some,
or even many. Please look in the code for **`bin/pyxie`** for the moment to
see how these are defined. The approach take will improve as time goes on,
and this is a stub - while we work things out.

Do get in contact (preferably by raising issues on github) if you need more
added.

### Will Other functions work?

Quite probably. The approach of identifying types for variables based on
how they're first used makes things a lot simpler. The reason for this
is because if we don't *need* to know what the type of something is to
transform it, we don't try to identify it.

This means that pyxie cannot perform type *verification* at present, and
it doesn't try. It may do at a later point in time. Primarily it looks
for clues as to types and works from there.

**PLEASE** let me know if:

* You try functions that aren't listed here, and find they work - I can
  add them to the list

* You try functions that aren't listed here, and find they don't work - I
  can add them to a todo list so that they can work later, or assist you
  in figuring it out. (Please remember though that this is not my day job,
  and I do have a life outside work too!)

When I say "get in contact" - I mean preferably by raising issues on github!


### Custom Arduino Types?

There are circumstances where the profile needs extending. The most
common examples of these are when objects get created like servos.
I'll hope to document later better how this gets sorted. For the moment,
take a look at how servos are defined in **`model/functions.py`**, and see
how you extend the profile.

I'm deferring documenting this in part because I think this will be in
a bit of flux for a while the best approach is identified.

## Is this Done?

No, far from it. It should be useful though at this stage, and with
additional usecases, it will become more useful!.


[ARDUINOEXAMPLE]: https://github.com/sparkslabs/pyxie/tree/master/examples/arduino
[SERVOEXAMPLE]: https://github.com/sparkslabs/pyxie/tree/master/examples/servo
[ANALOGEXAMPLE]: https://github.com/sparkslabs/pyxie/tree/master/examples/analog
[PUPPYEXAMPLE]: https://github.com/sparkslabs/pyxie/tree/master/examples/puppy


