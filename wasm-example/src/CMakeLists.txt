cmake_minimum_required(VERSION 3.1)
project(example CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(example example.cpp)
add_executable(main main.cpp)
target_link_libraries(main example)
