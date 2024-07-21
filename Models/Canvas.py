import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT
from matplotlib.figure import Figure
import numpy as np
from math import sqrt,log10

# Canvas Class: Contains Attributes relating to The Matplotlib canvas



class MatCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=400):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("#F2F2F2")
        self.axes = fig.add_subplot(111)
        super(MatCanvas, self).__init__(fig)

        self.XAxis=[] # XAxis values to be plotted
        self.YAxis=[] 

    # Generate YAxis values based on formula and Min/Max X-values
    def Formulate(self,formula,minimum,maximum):
        if(formula==""): self.XAxis=[]
        else: self.XAxis=np.arange(minimum,maximum+0.00001)
        self.YAxis=[]

        #Converting ^ sign to **, since in python ^ is for XOR operation
        for i in range(len(formula)):
            if(formula[i]=='^'): formula=formula[:i]+"**"+formula[i+1:]

        #Iterating to Obtain Y values (sensitive to 0.00001)
        for x in self.XAxis:
            self.YAxis.append(eval(formula))

    # Used to plot and Update canvas, called when Function/formula is updated, or Min/Max x values are changed
    def Plot(self):
        self.axes.cla()
        self.axes.plot(self.XAxis,self.YAxis)
        self.draw()
    
    #Updates Function, therefore update Plot (in real time)
    def FunctionUpdate(self,text,minimum,maximum):
        self.Formulate(text,minimum,maximum)
        self.Plot()
        self.Formula=text

   
   




    