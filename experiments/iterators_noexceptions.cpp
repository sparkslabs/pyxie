/*
 * Python Style Iterators in C++
 * 
 * Removed the usage of the macros to expand code to make changes easier to verify
 * Removed usage of exceptions to allow usage on Arduino
 * Added default value in the generator class, to allow standard value to return when "finished"
 * Restructured to start pulling out commonalities to turn into macros
 * 
 */

#include <iostream>

#define GENERATOR_START if (this->__generator_state == -1) { return __default_value; } switch(this->__generator_state) { default:
#define YIELD(value)    this->__generator_state = __LINE__; return ((value) );   case __LINE__:
#define GENERATOR_END    }; this->__generator_state = -1; return __default_value;

template<class T>
struct Iterator {
    virtual T next()=0;
    virtual bool completed()=0;
};

template<class T>
class Generator : public Iterator<T> {
  protected:
    int __generator_state;
  public:
    T __default_value;
    Generator() : __default_value(T()) {     };
    ~Generator() {     };
    virtual bool completed() { return __generator_state==-1; };
};


struct range : public Generator<int> {
    int maxCount;
    int index;
    range(int max) :maxCount(max), index(0) {     };
    ~range() {     };
  
    virtual int next() {
        GENERATOR_START

        while (index<maxCount) {
            YIELD(index);
            index += 1;
        }

        GENERATOR_END
    }
};


struct strlist : public Generator<std::string> {
    strlist()  {     };
    ~strlist() {     };
  
    virtual std::string next() {
        GENERATOR_START

        YIELD("Mary");
        YIELD("had");
        YIELD("a");
        YIELD("little");
        YIELD("lamb");
        YIELD("its");
        YIELD("fleece");
        YIELD("as");
        YIELD("white");
        YIELD("as");
        YIELD("snow");

        GENERATOR_END
    }
};


int main(int argc, char* argv[]) {
    // Code to be replaced with a range() style iterator
    int count;
    std::string word;
    range range_gen = range(5);
    strlist strlist_gen = strlist();

    while (true) {
        count = range_gen.next();
        if (range_gen.completed())
            break;
        std::cout << count;
    }
    std::cout << "." << std::endl;

    while (true) {
        word = strlist_gen.next();
        if (strlist_gen.completed())
            break;
        std::cout << word << " ";
    }
    std::cout << "." << std::endl;

    return 0;
}
