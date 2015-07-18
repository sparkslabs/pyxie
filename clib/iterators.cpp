#include "iterators.hpp"

struct range : public Generator<int> {
    int maxCount;
    int index;
    range() :maxCount(0), index(0) {     };
    range(int max) :maxCount(max), index(0) {     };
    ~range() {     };

    virtual int next() {
    GENERATOR_CODE_START
    while (index<maxCount) {
         YIELD(index);
         index += 1;
    }
    GENERATOR_CODE_END
    }
};
