
from PySide2.QtWidgets import QApplication
from  Models.Interface import PlotterMain 
import sys

app=QApplication(sys.argv)
window=PlotterMain()
window.show()

app.exec_()