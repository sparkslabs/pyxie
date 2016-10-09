---
template: mainpanel
source_form: markdown
name: Example Arduino Servo Control Program
updated: October 2016
title: Example Arduino Servo Control Pyxie Program
reviewed: October 2016
---
Example Arduino Program using Servos

<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b> servo-test-target.pyxie

<pre>

    #include &lt;Servo.h&gt;

    myservo = Servo()
    pos = 0
    pin=11

    myservo.attach(pin)
    while True:
        for pos in range(180):
            myservo.write(pos)
            delay(15)

        for pos in range(180):
            myservo.write(179-pos)
            delay(15)
</pre>
</div>
<div class="column col3_5">
<b>Generated:</b> servo-test-target.ino
<pre>
#include &lt;Servo.h&gt;
&nbsp;
#include "iterators.cpp"
&nbsp;
void setup() {
    Servo myservo;
    int pin;
    int pos;
    range range_iter_1;
    range range_iter_2;

    pos = 0;
    pin = 11;
    (myservo).attach(pin);
    while (true) {

        range_iter_1 = range(180);
        while (true) {
            pos = range_iter_1.next();
            if (range_iter_1.completed())
                break;


            (myservo).write(pos);
            delay(15);          // Itself uses pos
        }
        ;

        range_iter_2 = range(180);
        while (true) {
            pos = range_iter_2.next();
            if (range_iter_2.completed())
                break;


            (myservo).write((179 - pos));
            delay(15);          // Itself uses pos
        }
        ;
    };
}
&nbsp;
void loop() {
}
</pre>
</div>
</div>


