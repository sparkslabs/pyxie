/*
 * Python Style Iterators in C++, based on prior work from Kamaelia
 * 
 */

// This is Code/CPP/Scratch/generators.hpp:

#include <iostream>
#include <exception>

#define GENERATOR_CODE_START  if (this->__generator_state == -1)      \
                     { throw StopIteration(); }         \
                     switch(this->__generator_state)         \
                     { default:
#define YIELD(v)         this->__generator_state = __LINE__; \
                         return (v);                         \
                         case __LINE__:
#define GENERATOR_CODE_END     };                                      \
                     this->__generator_state = -1; throw StopIteration();

class StopIteration : public std::exception {
  virtual const char* what() const throw()
  {
    return "StopIteration";
  }
};

template<class T>
struct Iterator {
    virtual T next() {  }
};

template<class T>
class Generator : public Iterator<T> {
  protected:
    int __generator_state;
  public:
    Generator()  {     };
    ~Generator() {     };
};


struct range : public Generator<int> {
    int maxCount;
    int index;
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

struct strlist : public Generator<std::string> {
    strlist()  {     };
    ~strlist() {     };
  
    virtual std::string next() {
    GENERATOR_CODE_START
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
    GENERATOR_CODE_END
    }
};

int main(int argc, char* argv[]) {
    // Code to be replaced with a range() style iterator
    int count;
    range range_gen = range(5);
    while (true) {
        try {
            count = range_gen.next();
        } catch (StopIteration s) {
            break;
        }
        std::cout << count;
    }
    std::cout << "." << std::endl;

    strlist strlist_gen = strlist();
    std::string word;
    while (true) {
        try {
            word = strlist_gen.next();
        } catch (StopIteration s) {
            break;
        }
        std::cout << word << " ";
    }
    std::cout << "." << std::endl;

    return 0;
}
