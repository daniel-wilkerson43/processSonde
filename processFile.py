import numpy as np
import sympy as sp
#import Nio as nio


'''
****GUIDE TO READING COMMENTS****
All comments in this file are to be read prior to reading
the function. If a function has green comments above it, 
they're notes on how the function works.
'''


'''
listFile uses the numpy function genfromtxt to pull data out of
Graw profile data. Make sure you save the Graw data as .txt, this
code won't like Excell or other formats. After genfromtxt, the
code prompts you to see if you want another file imported. The
while loop runs until a maximum of three files have been imported,
or the user chooses to end the loop. Function returns three data
sets, make sure if you're only using one to specify listFile(xxx)[0].
'''

def listFile(fileName, sHeader, sFooter): 
    data1 = np.genfromtxt(fileName, skip_header=sHeader, skip_footer=sFooter, unpack=False)
    return data1

'''
isolateValues pulls all values from one column of data and returns
a list of those values. Pretty simple stuff.
'''
    
def isolateValues(data, columnValue): 
    value = data[:, columnValue]
    return value
  
'''
makeArray just passes a list (Or, frankly, anything you pass in)
in and returns an array of that list. Just a step to ensure you can
perform math operations on the data.
'''
  
def makeArray(data): 
    arrayData = np.array(data)
    return arrayData
   
'''
cutData takes in two lists of values of equal length, and a
upper and lower limit for the first list. It pulls all values
in that range out of the first list, and all values at the same
index value from the second list.
'''   
   
def cutData(data1, data2, lowerLimit, upperLimit):
    newData1 = []
    newData2 = []
    for i in range(len(data1)):
        if upperLimit == -1000:
            break
        if data1[i] >= lowerLimit and data1[i] <= upperLimit:
            newData1.append(data1[i])
            newData2.append(data2[i])
        elif data1[i] > upperLimit:
            break
    return newData1, newData2

'''
uncertaintyList just takes a list of values that you need
uncertainties for, the value of the uncertainty of your measurement,
and generates a list filled with the uncertainty value whose length
is equal to the length of the data list.
'''
    
def uncertaintyList(data, uValue):
    uList = []
    for i in range(len(data)):
        uList.append(uValue)
    return uList

'''
findIsotherm attempts to find the location of the tropopause
by checking nearby temperature values to see if they're changing
at a greatly reduced rate. If they are, it could be an indicator
of the tropopause. The value of the altitude at the same list location
as the reduced temperature gradient is returned.
'''

def findIsotherm(temperatures, altitudes):
    iterator = 0    
    iso = 0
    previousValue = 0    
    for i in temperatures:
        if iso == 3:
            iterator = iterator - 3
            isovalue = altitudes[iterator]
            break
        if i < previousValue - 1 or i > previousValue + 1:
            previousValue = i
            iso = 0
        else:
            if altitudes[iterator] > 8000:
                iso += 1
                previousValue = i
            else:
                iso = 0
        iterator += 1
    return iterator, isovalue
    
'''
leastSquarePolyfit uses the numpy polynomial polyfit function to
obtain the slope and y-intercept of the best fit line.
'''    
    
def leastSquarePolyfit(x, y, yUncertainty):
    b, m = np.polynomial.polynomial.polyfit(x,y,1,w=yUncertainty)
    fit = (m*x + b)
    return b, m, fit
        
'''
leastSquareLinalg uses the numpy linear algebra least squares method to
generate the slope and y-intercept for the linear least square fit
line. A is a matrix of the values of y and 1, and this is passed
into the linalg.lstsq function. I'll be honest, I don't really
understand perfectly how this function works so I don't use it much.
Might be worth digging into the numpy code to find out why it works
the way it works at some point.
'''

def leastSquareLinalg(x, y):
    A = np.vstack([y, np.ones(len(y))]).T
    m, c = np.linalg.lstsq(A, x)[0]
    return m, c
   
'''
customLeastSquare is the least square method from An Introduction to
Error Analysis. Very useful book. If you want to see where the 
equations came from, look it up. Pretty simple math here, not much
else to see.
'''
   
def customLeastSquare(x, y):
    sumX = sum(x)
    sumXSquared = sum(x**2)
    sumY = sum(y)
    sumXY = sum(x*y)
    N = len(x)
    delta = N*sumXSquared - sumX**2
    A = (sumXSquared*sumY - sumX*sumXY)/delta
    B = (N*sumXY - sumX*sumY)/delta
    return B, A

'''
differentiate does exactly what it says it does. You pass in
a list of values, a function that models them, and a rate of 
change and using the limit definition of a derivative, it finds
a list of differentiated values.
'''

def differentiate(function, yList, dx):
    dyList = []
    for i in yList:
        deriv = (function(i + dx) - function(i))/dx
        dyList.append(sp.limit(deriv, dx, 0))
    return dyList

'''
upperTrop uses the derivative of the best fit line for altitude
versus wind speed and finds the 0 of the derivative, and uses it
as a potential upper troposphere point.
'''

def upperTrop(function, x, dx):
    test = differentiate(function, x, dx)
    minTest = min(float(s) for s in np.abs(test))
    for i in range(len(test)):
        if test[i] == minTest:
            return x[i]            

'''
relativeUncertainty lets you compare the fractional uncertainty
in two different values. Pass in, for example, temperature and
altitude and their known uncertainties. It'll return an average
of those values, which should put you in the right ballpark.
'''
    
def relativeUncertainty(dy, y, dx, x):
    Y = 0
    X = 0
    for i in y:
        Y += i
    for i in x:
        X += i
    avgY = Y/len(y)
    avgX = X/len(x)
    relativeX = dx[0]/avgX
    relativeY = dy[0]/avgY
    return relativeX, relativeY

'''
Searches for the associated altitude to the given tropopause 
pressure.
'''
        
def checkPressureGraw(data, tropo):        
    tropAlt = 0 
    iterator = 0
    for i in data[:,1]:
        if i == tropo:
            tropAlt = data[iterator, 8]
        if i <= tropo:
            if tropAlt != 0:
                break
            elif tropAlt == 0:
                tropAlt = data[iterator, 8]
        iterator += 1
    return tropAlt

'''
polyFit takes in an x and y, the degree of the required polynomial, and
the number of points to return and returns a best fit polynomial.
'''

def polyFit(x, y, degree, numPoints):
    p = np.polyfit(x, y, degree)
    f = np.poly1d(p)
    print "Polyfit polynomial = " + str(f)
    x_new = np.linspace(x[0], x[-1], numPoints)
    y_new = f(x_new)
    return x_new, y_new, f
'''
grawValues pulls a designated column of data out
of the graw text file for plotting.
'''

def grawValues(fileName, sHeader, sFooter, column1):
    data = listFile(fileName, sHeader, sFooter)
    data1 = isolateValues(data, column1)
    v1Array = makeArray(data1)
    return v1Array

'''
latLongDiff takes a list of latitudes and a list of longitudes and
returns the differences between each point. Currently non-functioning,
returning extraneous points drastically outside of the path.
'''

def latLongDiff(lats, longs):
    avgLongs = []
    avgLats = []
    for i in range(len(longs)):
        if (i+1) == len(longs):
            break
        avgLongs.append(longs[i] - longs[i+1])
    for i in range(len(lats)):
        if (i+1) == len(lats):
            break
        avgLats.append(lats[i + 1] - lats[i])
    avgLat = sum(np.abs(avgLats))/len(avgLats)
    avgLong = sum(np.abs(avgLongs))/len(avgLongs)
    new_lats = []
    new_longs = []
    for i in range(len(lats)):
        if (i+1) == len(lats):
            break
        temp_value = (np.abs(lats[i+1]) - np.abs(lats[i]))
        if temp_value > avgLat*2:
            new_lats.append(avgLat)
        elif temp_value <= avgLat*2:
            new_lats.append(temp_value)
    for i in range(len(longs)):
        if (i+1) == len(longs):
            break
        temp_value = (np.abs(longs[i]) - np.abs(longs[i+1]))
        if temp_value > avgLong*2:
            new_longs.append(avgLong)
        elif temp_value <= avgLong*2:
            new_longs.append(temp_value)
    return new_lats, new_longs

'''
isolateDisc takes in an upper and lower limit in altitudes desired, an
altitude list (z), x and y lists, and returns all x and y values in that
altitude range.
'''

def isolateDisc(lowerLimit, upperLimit, z, x, y):
    positionValue = []
    for i in range(len(z)):
        if z[i] > lowerLimit and z[i] < upperLimit:
            positionValue.append(i)
    newX = []
    newY = []
    for i in positionValue:
        newX.append(x[i])
        newY.append(y[i])
    return newX, newY, positionValue

'''
deltaAFlattening takes in a list and a desired
range for change. It then forces all values on that list
to be the same for said range. Follows the rule for rounding
where below 5 forces to the lower value and above 5 forces to 
the upper value.
'''

def deltaAFlattening(altitudes, deltaA):
    flattenedA = []
    iterator = 1
    totalDiscs = (altitudes[len(altitudes)-1]-altitudes[0])/deltaA    
    print("Total number of discs: " + str(totalDiscs))
    for i in range(len(altitudes)):
        if iterator <= totalDiscs or len(flattenedA) < len(altitudes):
            if (altitudes[0] + (deltaA * iterator)) < altitudes[i]:
                iterator += 1
            if (altitudes[i] - (altitudes[0] + (deltaA * (iterator - 1))) < ((altitudes[0] + (deltaA * iterator)) - altitudes[i])):
                flattenedA.append(altitudes[0] + (deltaA * (iterator - 1)))
            elif (altitudes[i] - (altitudes[0] + (deltaA * (iterator - 1))) >= ((altitudes[0] + (deltaA * iterator)) - altitudes[i])):
                flattenedA.append(altitudes[0] + (deltaA * iterator))
        elif len(flattenedA) == len(altitudes):
            break
    return flattenedA
        
        
'''
convertVector takes a vector magnitude and direction in and
returns the xy coordinates.
'''

def convertVector(magnitude, direction):
    xValues = []
    yValues = []
    for i in range(len(magnitude)):
        xValues.append(magnitude[i]*np.cos(direction[i]))
        yValues.append(magnitude[i]*np.sin(direction[i]))
    xArray = makeArray(xValues)
    yArray = makeArray(yValues)
    return xArray, yArray

'''
grawProfileLists is a function specifically for pulling data out of
Grawmet generated profile data table text files. It utilizes the 
functions above.
'''        
        
def grawProfileLists(fileName, sHeader, sFooter, column1, column2, PBL, uncertaintyX, uncertaintyY):
    data = listFile(fileName, sHeader, sFooter) #Create a list from data     
    try:    
        trop = "Tropopause:"
        trop1 = 0
        search = open(fileName)
        for line in search:
            if trop in line:
                trop1 = line[15:18]
                print "Tropopause given by Graw: " + str(trop1) + "mb"
                break
        tropAlt = checkPressureGraw(data, int(trop1)) - 1000
        if tropAlt == -1000:
            print "No Graw defined tropopause. Attempting to estimate..."
        else:
            print "Tropopause altitude defined by Graw - 1000: " + str(tropAlt) + " meters"
        dataT = isolateValues(data, column1) #Isolate the temperature column in a new list
        dataA = isolateValues(data, column2) #Isolate the altitude column in a new list
        aCutData, tCutData = cutData(dataA, dataT, PBL, tropAlt)        
        tArray = makeArray(tCutData) #Turn the cut temperature list into an array for processing
        aArray = makeArray(aCutData)/1000 #Turn the cut altitude list into an array for processing
        aUList = uncertaintyList(aArray, uncertaintyY)#Create a list of uncertainties for altitudes
        tUList = uncertaintyList(tArray, uncertaintyX)#Create a list of uncertainties for temperatures
        tUArray = makeArray(tUList)    
        aUArray = makeArray(aUList)#Turn the altitude uncertainty list into an array
        rX,rY = relativeUncertainty(aUList, aCutData, tUList, tCutData)
    except ZeroDivisionError:
        dataT = isolateValues(data, column1) #Isolate the temperature column in a new list
        dataA = isolateValues(data, column2) #Isolate the altitude column in a new list
        iValue, pTrop = findIsotherm(dataT, dataA)
        tropCheck = raw_input("Search found " + str(pTrop) + " as a possible tropopause for Graw. Use this value? y/n:")
        if tropCheck == "y":
            opCheck = raw_input("Plus or minus 1000? +/-/n: ")
            if opCheck == "+":
                trop = pTrop + 1000
            elif opCheck == "-":
                trop = pTrop - 1000
            elif opCheck == "n":
                trop = pTrop
        elif tropCheck == "n":
            trop = raw_input("Enter an approximate tropopause: ")        
        aCutData,tCutData = cutData(dataA, dataT, PBL, int(trop))#Cut unnecessary data from the altitude list
        tArray = makeArray(tCutData) #Turn the cut temperature list into an array for processing
        aArray = makeArray(aCutData)/1000 #Turn the cut altitude list into an array for processing
        aUList = uncertaintyList(aArray, uncertaintyY)#Create a list of uncertainties for altitudes
        tUList = uncertaintyList(tArray, uncertaintyX)#Create a list of uncertainties for temperatures
        tUArray = makeArray(tUList)    
        aUArray = makeArray(aUList)#Turn the altitude uncertainty list into an array
        rX,rY = relativeUncertainty(aUList, aCutData, tUList, tCutData)
        return tArray, aArray, tUArray, aUArray, rX, rY, trop
        
    return tArray, aArray, tUArray, aUArray, rX, rY, tropAlt/1000
  
        
'''
Much like grawProfileLists above, wwwSoundingLists pulls data from 
Wyoming Weather Web values. There are no temperature or altitude 
uncertainties here, since the values are interpolated.
'''        
        
def wwwSoundingLists(fileName, sHeader, sFooter, column1, column2, PBL):
    data = listFile(fileName, sHeader, sFooter)
    dataT = isolateValues(data, column1)
    dataA = isolateValues(data, column2)
    iValue, pTrop = findIsotherm(dataT, dataA)
    tropCheck = raw_input("Search found " + str(pTrop) + " as a possible tropopause for WWW. Use this value? y/n:")
    if tropCheck == "y":
        opCheck = raw_input("Plus or minus 1000? +/-/n: ")
        if opCheck == "+":
            trop = pTrop + 1000
        elif opCheck == "-":
            trop = pTrop - 1000
        elif opCheck == "n":
            trop = pTrop
    elif tropCheck == "n":
        trop = raw_input("Enter an approximate tropopause: ")
    aCutData, tCutData = cutData(dataA, dataT, PBL, int(trop))
    tArray = makeArray(tCutData)
    aArray = makeArray(aCutData)/1000
    return tArray, aArray

'''
As above. Takes tabular data from the SPC website and pulls the
required temperature and altitude values. Again, uncertain of errors
so none are associated here.
'''

def spcProfileLists(fileName, sHeader, sFooter, column1, column2, PBL):
    data = np.genfromtxt(fileName, skip_header=sHeader, skip_footer=sFooter, delimiter=",", unpack=False)
    dataT = isolateValues(data, column1)
    dataA = isolateValues(data, column2)
    iValue, pTrop = findIsotherm(dataT, dataA)
    tropCheck = raw_input("Search found " + str(pTrop) + " as a possible tropopause for SPC. Use this value? y/n:")
    if tropCheck == "y":
        opCheck = raw_input("Plus or minus 1000? +/-/n: ")
        if opCheck == "+":
            trop = pTrop + 1000
        elif opCheck == "-":
            trop = pTrop - 1000
        elif opCheck == "n":
            trop = pTrop
    elif tropCheck == "n":
        trop = raw_input("Enter an approximate tropopause: ")
    aCutData, tCutData = cutData(dataA, dataT, PBL, int(trop))
    tArray = makeArray(tCutData)
    aArray = makeArray(aCutData)/1000
    return tArray, aArray

'''
propUncertainty takes the uncertainty in x and y, the values of x
and y, and the new value made from x and y called z and multiplies
z by the square root of the fractional uncertainties squared added
together to produce the uncertainty in z.
'''

def propUncertainty(x, dx, y, dy, z):
    dz = []    
    dzAvg = 0
    for i in range(len(x)):
        dz.append(z*np.sqrt((dx/x[i])**2 + (dy/y[i])**2))
    for i in dz:
        dzAvg += i
    dzTotal = dzAvg/len(dz)
    return dzTotal

'''
This section is a work in progress. Will be used to import values
from a WRF run to verify the values against radiosonde soundings.
'''
        
#def processWRF(fileName, fileFormat):
#    f = nio.open_file(fileName, format=fileFormat)
#    readvarphb = "PHB"
#    readvarph = "PH"
#    readvart = "T"
#    ph = np.array(f.variables[readvarph][:])
#    phb = np.array(f.variables[readvarphb][:])
#    t = np.array(f.variables[readvart][:])
#    altitude = (ph+phb)/9.81
#    return t, altitude
    
