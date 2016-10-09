---
template: mainpanel
source_form: markdown
name: Example Arduino Program
updated: October 2016
title: Example Arduino Pyxie Program
reviewed: October 2016
---
Basic Arduino Example

<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b> arduino-for-blink.pyxie

<pre>
    led = 13;

    pinMode(led, OUTPUT);

    while True:
        for i in range(6):
            digitalWrite(led, HIGH)
            delay(200)
            digitalWrite(led, LOW)
            delay(200)
        delay(1000)
</pre>
</div>
<div class="column col3_5">
<b>Generated:</b> arduino-for-blink.ino
<pre>
#include "iterators.cpp"
&nbsp;
void setup()
{
    int i;
    int led;
    range range_iter_1;
    led = 13;
    pinMode(led, OUTPUT);
    while(true) {
        range_iter_1 = range(6);
        while (true) {
            i = range_iter_1.next();
            if (range_iter_1.completed())
                break;
             digitalWrite(led, HIGH);
             delay(200);
             digitalWrite(led, LOW);
             delay(200);
        };
        delay(1000);
    };
}
&nbsp;
void loop()
{
}
</pre>
</div>
</div>

