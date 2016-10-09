---
template: mainpanel
source_form: markdown
name: Example Analog Demo Arduino Program
updated: October 2016
title: Example Analog Demo Arduino Pyxie Program
reviewed: October 2016
---
Analog, serial demo Arduino program:

<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b> analog/analog-serial.pyxie

<pre>
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
</pre>
</div>
<div class="column col3_5">
<b>Generated:</b> analog-serial.ino
<pre>
#include "iterators.cpp"
&nbsp;
#include "iterators.cpp"
&nbsp;
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
&nbsp;
void loop() {
}
</pre>
</div>
</div>
