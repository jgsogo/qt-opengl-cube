#pragma once

#ifdef WIN32
  #define example_EXPORT __declspec(dllexport)
#else
  #define example_EXPORT
#endif

example_EXPORT void example();
