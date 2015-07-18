---
template: mainpanel
source_form: markdown
name: Example Program
updated: July 2015
title: Representative Pyxie Program
---
Example program:

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

Example results:

    #include <iostream>
    #include <string>

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
        cout << ((10-1)-2) << " " << 7 << endl;
        cout << ((1+((2*3)*4))-(5/7)) << " " << 25 << endl;
        cout << age << " " << new_age << " " << new_age_too << endl;
        cout << foo << " " << bar << " " << foobar << endl;
        countdown = 2147483647;
        cout << "COUNTING DOWN" << endl;
        while(countdown) {
            countdown = (countdown-1);
        };
        cout << "BLASTOFF" << endl;
        return 0;
    }
