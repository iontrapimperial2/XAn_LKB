#include "xan.h"
#include "ui_xan.h"

XAn::XAn(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::XAn)
{
    ui->setupUi(this);
}

XAn::~XAn()
{
    delete ui;
}
