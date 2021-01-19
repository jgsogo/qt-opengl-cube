#include <QOpenGLWindow>
#include <QColor>
#include <QOpenGLShaderProgram>

class HelloWindow : public QOpenGLWindow
{
public:
    HelloWindow();

private:    
    void updateColor();

    void initializeGL() override;
    void resizeGL(int w, int h) override;
    void paintGL() override;

    void mousePressEvent(QMouseEvent *) override;
    void keyPressEvent(QKeyEvent* event) override;
    
    int m_colorIndex;
    QColor m_color;
    bool m_animating;

    void paintQtLogo();
    void createGeometry();
    void createBubbles(int number);
    void quad(qreal x1, qreal y1, qreal x2, qreal y2, qreal x3, qreal y3, qreal x4, qreal y4);
    void extrude(qreal x1, qreal y1, qreal x2, qreal y2);
    QVector<QVector3D> vertices;
    QVector<QVector3D> normals;
    qreal m_fAngle;
    int vertexAttr;
    int normalAttr;
    int matrixUniform;
    int colorUniform;

    QSurfaceFormat m_format;
    QOpenGLContext *m_context;
    QOpenGLShaderProgram *m_program;
};
