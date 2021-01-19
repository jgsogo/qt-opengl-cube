#include <iostream>
#include "example.h"

void example(){
    #ifdef NDEBUG
    std::cout << "example/version: Hello World Release!" <<std::endl;
    #else
    std::cout << "example/version: Hello World Debug!" <<std::endl;
    #endif
}
