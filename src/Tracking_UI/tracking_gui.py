from PyQt5 import QtCore, QtGui, QtWidgets
from QLed import QLed
from generated_ui import Ui_UEWS_Tracking_GUI

def init_light(qled: QLed):
    qled.setOffColour(QLed.Red)
    qled.setOnColour(QLed.Green)
    qled.setShape(QLed.Square)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UEWS_Tracking_GUI = QtWidgets.QMainWindow()
    ui = Ui_UEWS_Tracking_GUI()
    ui.setupUi(UEWS_Tracking_GUI)

     # Configure Lights
    for name in vars(ui):
        var = vars(ui)[name]
        if type(var) is QLed:
            init_light(var)

    ui.send_warn_tones_indicator.setOnColour(QLed.Yellow)
    ui.send_warn_tones_indicator.setOffColour(QLed.Grey)
    ui.alarm_enable_indicator.setOnColour(QLed.Yellow)
    ui.alarm_enable_indicator.setOffColour(QLed.Grey)
    ui.alarm_on_indicator.setOnColour(QLed.Red)
    ui.alarm_on_indicator.setOffColour(QLed.Grey)

    UEWS_Tracking_GUI.show()
    sys.exit(app.exec_())