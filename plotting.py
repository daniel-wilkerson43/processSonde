import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
    
def numPlots(total):
    d = {}
    for i in range(total):
        d["ax" + str(i)] = 0
    return d

def threeDScatterPlot(figure, x, y, z, xLabel, yLabel, zLabel):
    figure = plt.figure()    
    ax = Axes3D(figure)
    ax.scatter(x, y, z)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_zlabel(zLabel)
    
    
def threeDLinePlot(figure, x, y, z, xLabel, yLabel, zLabel):
    figure = plt.figure()    
    ax = Axes3D(figure)
    ax.plot(x, y, z)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_zlabel(zLabel)
    
    
def scatterAndFitLine(figure, x, y, y2, xLabel, yLabel, title, title2, xErr=None):    
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.scatter(x, y, label=title)
    ax.plot(x, y2, label=title2)
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.errorbar(x, y, yerr=None, xerr=xErr, fmt=None)
    

def scatterPlot(figure, x, y, xLabel, yLabel, title):
    figure = plt.figure()
    ax = figure.add_subplot(111)    
    ax.scatter(x, y, label=title)
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    ax.xlabel(xLabel)
    ax.ylabel(yLabel)
    
def linePlot(figure, x, y, xLabel, yLabel, title):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.plot(x, y, label=title)
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    
def polarPlot(figure, x, y, layers):
    figure = plt.figure()    
    ax1 = figure.add_subplot(111, polar = True)
    ax1.set_theta_offset(np.pi/2)
    ax1.set_theta_direction(-1)
    ax1.plot(x,y)#,'ro-')
    ax1.set_title("Windspeed vs. direction from " + layers)
    
def lineBestFit(figure, x, y, x_new, y_new, xLabel, yLabel, title):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.plot(x, y, label=title)
    ax.plot(x_new, y_new, label="Best fit polynomial")
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    