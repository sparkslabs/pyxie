Analog Example
--------------

Spelling note: this is spelt analog, rather than analogue because that's the
spelling in the API. I normally prefer UK spellings for things for obvious
reasons, but in this case consistency makes sense.

The purpose of this example is to provide a practical test for creating and
testing the following API and language elements:

   * Support for profile defined variables - such as A0
   * Support for profile defined objects - such as Serial
   * Support for proifle defined functions - such as analogRead, analogWrite

Furthermore it (unintentionally) caused the need to turn "print" from being a
separate syntactic value to being a function. This is necessary to support
things like Serial.print. This is a little frustrating because I'd hoped to
deal with this later, but it's such an important change, it needs to happen
sooner rather than later.


### Current Source

    analogInPin = A0
    analogOutPin = 9
    sensorValue = 0
    outputValue = 0
    Serial.begin(9600)
    randomTest = 0
    randomSeed(analogRead(0))

    while True:
        sensorValue = analogRead(analogInPin)
        sensorValue = constrain(sensorValue, 10, 150);
        outputValue = map(sensorValue, 0, 1023, 0, 255)
        randomTest = random(300)
        analogWrite(analogOutPin, outputValue)
        Serial.print(millis())
        Serial.print(" : ")
        Serial.print("sensor:- ")
        Serial.print(sensorValue)
        Serial.print(" output:- ")
        Serial.print(outputValue)
        Serial.print(" random:- ")
        Serial.print(randomTest)
        Serial.println("--------")
        delay(2)

### Generated C++

    #include "iterators.cpp"

    void setup() {
        int analogInPin;
        int analogOutPin;
        int outputValue;
        int randomTest;
        int sensorValue;

        analogInPin = A0;
        analogOutPin = 9;
        sensorValue = 0;
        outputValue = 0;
        (Serial).begin(9600);
        randomTest = 0;
        randomSeed(analogRead(0));
        while (true) {
            sensorValue = analogRead(analogInPin);
            sensorValue = constrain(sensorValue, 10, 150);
            outputValue = map(sensorValue, 0, 1023, 0, 255);
            randomTest = random(300);
            analogWrite(analogOutPin, outputValue);
            (Serial).print(millis());
            (Serial).print(" : ");
            (Serial).print("sensor:- ");
            (Serial).print(sensorValue);
            (Serial).print(" output:- ");
            (Serial).print(outputValue);
            (Serial).print(" random:- ");
            (Serial).print(randomTest);
            (Serial).println("--------");
            delay(2);
        };
    }

    void loop() {
    }
