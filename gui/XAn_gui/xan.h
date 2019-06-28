#ifndef XAN_H
#define XAN_H

#include <QMainWindow>

namespace Ui {
class XAn;
}

class XAn : public QMainWindow
{
    Q_OBJECT

public:
    explicit XAn(QWidget *parent = 0);
    ~XAn();

private:
    Ui::XAn *ui;
};

#endif // XAN_H
