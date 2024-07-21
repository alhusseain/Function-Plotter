from PySide2.QtWidgets import QMainWindow,QPushButton,QGridLayout,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QSizePolicy,QLineEdit,QDoubleSpinBox
from PySide2.QtCore import Qt
from Models.Canvas import *
import numpy as np


# This is the Main Window of the app
class PlotterMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plotter") # Name of the app
        

        
        MainLayout=QVBoxLayout()
        MainLayout.addStretch()


        Title=QLabel("Plotter™")
        Title.setStyleSheet("font-size:40pt; margin-left:40px;")
        Title.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        MainLayout.addWidget(Title,alignment=Qt.AlignHCenter)

        self.Canvas=MatCanvas(self,width=6,height=5,dpi=100)
        self.Canvas.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.Canvas.Plot()

        MainLayout.addWidget(self.Canvas,alignment=Qt.AlignHCenter)



        bar=QHBoxLayout()
        bar.addStretch()


        InputAndCheck=QVBoxLayout()
        InputAndCheck.addStretch()
        self.CheckLabel=QLabel()
        InputAndCheck.addWidget(self.CheckLabel,alignment=Qt.AlignLeft)
        
        # Function Box
        self.InputFunction=QLineEdit()
        self.InputFunction.setPlaceholderText("Input your function")
        self.InputStyle= """    
                                border-style:solid; 
                                border-width:3 3 3 3;
                                width:350px;
                                height: 45px;
                        """
        self.InputFunction.setStyleSheet(self.InputStyle)
        self.InputFunction.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        #bar.addWidget(InputFunction)
        self.InputFunction.textChanged.connect(self.ValidateAndUpdate)
        InputAndCheck.addWidget(self.InputFunction,alignment=Qt.AlignHCenter)
        InputAndCheck.setContentsMargins(0,0,0,25)
        InputAndCheck.addStretch()
        bar.addLayout(InputAndCheck)
        #---------------------------------------------------------------

        # Vertical Layout for the X range
        RangeInput=QVBoxLayout()
        RangeInput.addStretch()

        self.XMin=QDoubleSpinBox()
        self.XMin.setSingleStep(0.1)
        self.XMin.setSuffix(" (X-Min)")
        self.XMin.setMinimum(-1000000) # Allow negative input, limit to -+ 1000000 prevent program from crashing
        self.XMin.setMaximum(1000000)
        self.XMin.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.XMin.valueChanged.connect(self.UpdateXMin)
        self.XMin.setStyleSheet("width:125px;")
        

        self.XMax=QDoubleSpinBox()
        self.XMax.setSingleStep(0.1)
        self.XMax.setMaximum(1000000)
        self.XMax.setValue(5)
        self.XMax.setSuffix(" (X-Max)")
        self.XMax.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.XMax.valueChanged.connect(self.ValidateAndUpdate)

        RangeInput.addWidget(self.XMin)
        RangeInput.addWidget(self.XMax)

        RangeInput.addStretch()
        bar.addLayout(RangeInput)
        
        #---------------------------------------------------------------

        bar.addStretch()
        bar.setContentsMargins(10,0,0,50)

        MainLayout.addLayout(bar)

        MainLayout.addStretch()



        Display=QWidget()
        Display.setLayout(MainLayout)
        self.setCentralWidget(Display)


    # Used to Validate first the input function. If a correct Function, then graph is plotted, else specified error appears
    def ValidateAndUpdate(self):
        formula=self.InputFunction.text()
        minimum=self.XMin.value()
        maximum=self.XMax.value()

        if(formula==""): # if formula empty, erase plot and returns to starting look of program
            self.InputFunction.setStyleSheet(self.InputStyle)
            self.CheckLabel.setText("")
            self.Canvas.FunctionUpdate(formula,minimum,maximum)
            return
        if(formula.__contains__("**")): #special case since having ** wouldn't normally cause an error
                self.CheckLabel.setStyleSheet("color:#FF0000;")
                self.InputFunction.setStyleSheet(self.InputStyle+"border-color:#FF0000;")
                self.CheckLabel.setText("Incorrect Formula") 
                return
        if(formula.__contains__("/0")): # Not all /0 raise division by zero, so special case here
            self.CheckLabel.setStyleSheet("color:#FF0000;")
            self.InputFunction.setStyleSheet(self.InputStyle+"border-color:#FF0000;")
            self.CheckLabel.setText("Division By zero Detected !")
            return
        try: # if function is correct, displays chart
            self.Canvas.FunctionUpdate(formula,minimum,maximum)
            self.CheckLabel.setText("Correct!")
            self.CheckLabel.setStyleSheet("color:#008000;")
            self.InputFunction.setStyleSheet(self.InputStyle+"border-color:#008000;")
        
        # if error is caught, display the error
        #Note: 1/x or equivalent gives runtime Warning, when expected to give DivisionByZero error. This is fine by me, since having some sort of asymptote representation is welcomed, so won't handle it
        
        except ValueError: # ValueError - Cases: log10 with x<=0 // Sqrt with x<0 // Range is too big to process
            self.CheckLabel.setStyleSheet("color:#FF0000;")
            self.InputFunction.setStyleSheet(self.InputStyle+"border-color:#FF0000;")
            
            self.CheckLabel.setText("A <=0 value is entered inconveniently in log10 or sqrt")
        
        except ZeroDivisionError: # ZeroDivisionError - Means that a number was divided by zero
            self.CheckLabel.setStyleSheet("color:#FF0000;")
            self.InputFunction.setStyleSheet(self.InputStyle+"border-color:#FF0000;")
            
            self.CheckLabel.setText("Division By zero Detected !")
        
        except:   #Can only mean the formula was written incorrectly (errors Caught are SyntaxError and NameError)
                self.CheckLabel.setStyleSheet("color:#FF0000;")
                self.InputFunction.setStyleSheet(self.InputStyle+"border-color:#FF0000;")

                self.CheckLabel.setText("Incorrect Formula") 



    # This function updates the Xmin value, and also update the Minimum of XMax, ensuring that it doesn't go below XMin
    def UpdateXMin(self,value):
        self.ValidateAndUpdate()
        self.XMax.setMinimum(value+0.00001) # ensure that XMax does not get below current XMin value

      




        


