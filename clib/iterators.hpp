#ifndef PYXIE_ITERATORS_HPP
#define PYXIE_ITERATORS_HPP

/*
 * Python Style Iterators in C++, based in part on experiment work in Kamaelia
 * 
 */

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

#endif
