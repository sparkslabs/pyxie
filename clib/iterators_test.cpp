/*
 * Test of a C++ version of Python style generators.
 * 
 */

#include <iostream>
#include "iterators.cpp"
/*

While it may be a little unclear, this C++ program is equivalent
to this python program:

for count in range(5):
    print count,

print

It doesn't do this:

for(int count=0; count<5; count++) {
    std::cout << count;
}
std::cout << "." << std::endl;

Because doing it the way we do makes it avoid treating for/range as a
special case, meaning we solve the harder problem first.  Optimisations
specific to certain code structures can come later.

*/


int main(int argc, char* argv[]) {
    // Code to be replaced with a range() style iterator
    int count;
    range range_gen = range(5);

    while (true) {
        count = range_gen.next();
        if (range_gen.completed())
            break;
        std::cout << count;
    }
    std::cout << "." << std::endl;

    return 0;
}
