#include "iterators.hpp"

struct range : public Generator<int> {
    int start;
    int end;
    int step;

    int index;

    range() :                                start(0),     end(0),   step(1), index(0)            {     };
    range(int end) :                         start(0),     end(end), step(1), index(0)            {     };
    range(int start, int end)     :          start(start), end(end), step(1), index(start)        {     };
    range(int start, int end, int stepsize): start(start), end(end), step(stepsize), index(start) {     };
    ~range() {     };

    virtual int next() {
        GENERATOR_START

        while ( step>0  ? index < end : index > end) {
            YIELD(index);
            index = index + step;
        }

        GENERATOR_END
    }
};
