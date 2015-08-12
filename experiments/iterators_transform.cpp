/*
 * Python Style Iterators in C++
 * 
 * Removed the usage of the macros to expand code to make changes easier to verify
 * Removed usage of exceptions to allow usage on Arduino
 * Added default value in the generator class, to allow standard value to return when "finished"
 * 
 */

#include <iostream>
#include <exception>

template<class T>
struct Iterator {
    virtual T next() {  }
};

template<class T>
class Generator : public Iterator<T> {
  public:
    T __default_value;
    int __generator_state;
    Generator() : __default_value(T()) {     };
    ~Generator() {     };
};

struct range : public Generator<int> {
    int maxCount;
    int index;
    range(int max) :maxCount(max), index(0) {     };
    ~range() {     };
  
    virtual int next() {
        if (this->__generator_state == -1) {
            return __default_value;
        }
        switch(this->__generator_state) {
            default:
                    while (index<maxCount) {
                    this->__generator_state = __LINE__; return (index);  case __LINE__:
                    index += 1;
                }
        };
        this->__generator_state = -1;
        return __default_value;
    }
};

struct strlist : public Generator<std::string> {
    strlist()  {     };
    ~strlist() {     };
  
    virtual std::string next() {
        if (this->__generator_state == -1)  {
            return __default_value;
        }
        switch(this->__generator_state) {
            default:
            this->__generator_state = __LINE__; return ("Mary");   case __LINE__: ;
            this->__generator_state = __LINE__; return ("had");    case __LINE__: ;
            this->__generator_state = __LINE__; return ("a");      case __LINE__: ;
            this->__generator_state = __LINE__; return ("little"); case __LINE__: ;
            this->__generator_state = __LINE__; return ("lamb");   case __LINE__: ;
            this->__generator_state = __LINE__; return ("its");    case __LINE__: ;
            this->__generator_state = __LINE__; return ("fleece"); case __LINE__: ;
            this->__generator_state = __LINE__; return ("as");     case __LINE__: ;
            this->__generator_state = __LINE__; return ("white");  case __LINE__: ;
            this->__generator_state = __LINE__; return ("as");     case __LINE__: ;
            this->__generator_state = __LINE__; return ("snow");   case __LINE__: ;
        };
        this->__generator_state = -1;
        return __default_value;
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
        if (range_gen.__generator_state==-1)
            break;
        std::cout << count;
    }
    std::cout << "." << std::endl;

    while (true) {
        word = strlist_gen.next();
        if (strlist_gen.__generator_state==-1)
            break;
        std::cout << word << " ";
    }
    std::cout << "." << std::endl;

    return 0;
}
