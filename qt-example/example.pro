
TEMPLATE = app
TARGET = hello_conan

CONFIG += static

HEADERS += hellowindow.h
SOURCES += hellowindow.cpp main.cpp

OBJECTS_DIR += .obj
MOC_DIR += .moc

