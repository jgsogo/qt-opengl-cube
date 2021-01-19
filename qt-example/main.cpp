#include "hellowindow.h"

#include <QtGui>
#include <QScreen>

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    
    HelloWindow window;
    window.showFullScreen();
    
    return app.exec();
}
