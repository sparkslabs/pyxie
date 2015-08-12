#ifndef PYXIE_ITERATORS_HPP
#define PYXIE_ITERATORS_HPP

/*
 * Python Style Iterators in C++, based in part on experiment work in Kamaelia
 * Redone to remove use of generators, so that this can be used on Arduino
 * 
 */

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

#endif
