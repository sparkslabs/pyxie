---
template: mainpanel
source_form: markdown
name: Example Program
updated: July 2015
title: Representative Pyxie Program
---
<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b>

<pre>
age = 10
new_age = 10 +1
new_age_too = age + 1
new_age_three = age + new_age_too
foo = "Hello"
bar = "World"
foobar = foo + bar

print 10-1-2,7
print 1+2*3*4-5/7,25
print age, new_age, new_age_too
print foo, bar, foobar

countdown = 2147483647
print "COUNTING DOWN"
while countdown:
    countdown = countdown - 1

print "BLASTOFF"
</pre>
</div>
<div class="column col3_5">
<b>Generated:</b>
<pre>
#include &lt;iostream&gt;
#include &lt;string&gt;

using namespace std;

int main(int argc, char *argv[])
{
    int age;
    string bar;
    int countdown;
    string foo;
    string foobar;
    int new_age;
    int new_age_three;
    int new_age_too;

    age = 10;
    new_age = (10+1);
    new_age_too = (age+1);
    new_age_three = (age+new_age_too);
    foo = "Hello";
    bar = "World";
    foobar = (foo+bar);
    cout &lt;&lt; ((10-1)-2) &lt;&lt; " " &lt;&lt; 7 &lt;&lt; endl;
    cout &lt;&lt; ((1+((2*3)*4))-(5/7)) &lt;&lt; " " &lt;&lt; 25 &lt;&lt; endl;
    cout &lt;&lt; age &lt;&lt; " " &lt;&lt; new_age &lt;&lt; " " &lt;&lt; new_age_too &lt;&lt; endl;
    cout &lt;&lt; foo &lt;&lt; " " &lt;&lt; bar &lt;&lt; " " &lt;&lt; foobar &lt;&lt; endl;
    countdown = 2147483647;
    cout &lt;&lt; "COUNTING DOWN" &lt;&lt; endl;
    while(countdown) {
        countdown = (countdown-1);
    };
    cout &lt;&lt; "BLASTOFF" &lt;&lt; endl;
    return 0;
}
</pre>
</div>
</div>
