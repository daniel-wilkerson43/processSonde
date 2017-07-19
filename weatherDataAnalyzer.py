import plotting as pl
import processFile as pF
import numpy as np

#############Define constants##################

'''
Constants chosen for data processing. Graw produces 5
unnecessary lines at the start of their profile output
data and 10 unnecessary files at the end. Wyoming weather web has
7 unnecessary lines on top and 1 on the end. It's worth mentioning
for future work that the tropopause as defined by Graw is the
10th line from the bottom of the file. processFile contains a function
to pull the Graw tropopause. PBL was chosen somewhat arbitrarily,
to ensure that we're well above the boundary layer. Uncertainty in
temperature comes from the Graw manual for the DFM-06, same with the
altitude.
'''
grawTimeColumn = 0
grawPressureColumn = 1
grawTempColumn = 2
grawWindSpeedColumn = 4
grawWindDirectionColumn = 5
grawAltColumn = 6
grawLongColumn = 8
grawLatColumn = 9

WWWTempColumn = 2
WWWAltColumn = 1

SPCTempColumn = 2
SPCAltColumn = 1

sHeaderWWW = 8
sFooterWWW = 1
sHeaderSPC = 7
sFooterSPC = 0
sHeaderGraw = 5 #Ignore all lines in the file prior to this
sFooterGraw = 10 #Ignore all lines in the file after this

PBL = 5000 #m
PBLkm = 5.000 #km
tUncertainty = 0.2 #Degrees Celsius
aUncertainty = .01 #km

'''
Change these variables as required for running the code.
'''

deltaAltitude = 2000 #m
lowerAltitude = 14000 #m
upperAltitude = 16000 #m
grawFileName = "profile_07282016FTMISSOULA_LENOVO_01_DFM_06.txt"
wwwFileName = "WWWGFS3"
spcFileName = "TFX_Tabular_Data.txt"

#############End define constants##############



#############Define data lists and arrays######

'''
This section is all about pulling data into the code and
evaluating it in a way that is useful for data processing.
See the processFile.py code for more information on the functions
being used here. Generally speaking, a filename is sent in
(make sure file to be read is in the same location as the code)
and then cut into the values we want to pull. (Temperature is the
2nd column, altitude is the 8th) After columns are separated into
their own lists, the data is passed into a cut function to remove
all data outside of our specified boundaries (5km for PBL, then
whatever the tropopause is defined as by Graw) and turned into
arrays so that math operations can be performed on them.
'''
lats = pF.grawValues(grawFileName, sHeaderGraw, sFooterGraw, grawLatColumn)
longs = pF.grawValues(grawFileName, sHeaderGraw, sFooterGraw, grawLongColumn)
time = pF.grawValues(grawFileName, sHeaderGraw, sFooterGraw, grawTimeColumn)
wSpeeds = pF.grawValues(grawFileName, sHeaderGraw, sFooterGraw, grawWindSpeedColumn)
wDirections = pF.grawValues(grawFileName, sHeaderGraw, sFooterGraw, grawWindDirectionColumn)
wAltitudes = pF.grawValues(grawFileName, sHeaderGraw, sFooterGraw, grawAltColumn)
pressures = pF.grawValues(grawFileName, sHeaderGraw, sFooterGraw, grawPressureColumn)

temperatures, altitudes, tUncertaintyList, aUncertaintyList, rX, rY, trop \
= pF.grawProfileLists(grawFileName, sHeaderGraw, sFooterGraw, grawTempColumn, grawAltColumn, PBL, tUncertainty, aUncertainty)

tWWW, aWWW = pF.wwwSoundingLists(wwwFileName, sHeaderWWW, sFooterWWW, WWWTempColumn, WWWAltColumn, PBL)
tSPC, aSPC = pF.spcProfileLists(spcFileName, sHeaderSPC, sFooterSPC, SPCTempColumn, SPCAltColumn, PBL)

##########End define data lists and arrays######



############Best fit line section##############

'''
Three different methods of generating a linear
least square fit are available in processFile. 
All three have been tested against each other using the same 
data set, and produce the same result. I'm settling on using 
the customLeastSquare function I wrote in processFile, since it's taken
straight from An Introduction to Error Analysis, by John R. Taylor,
and I feel the most confident in understanding the process from
start to finish. The other two are perfectly viable options,
however. There is also a polynomial best fit line included in
processFile.
'''

m3, b3 = pF.customLeastSquare(temperatures, altitudes)
lapseRate = m3**-1
dz = pF.propUncertainty(temperatures, tUncertainty, altitudes, aUncertainty, np.abs(lapseRate))
print "Lapse rate for Grawmet profile data: %.2f" %lapseRate + " +- %.2f" % round(dz,2) + " degrees C per km"
fitC = (m3*temperatures + b3)

mW, bW = pF.customLeastSquare(tWWW, aWWW)
lapseRateW = mW**-1
print "Lapse rate for Wyoming Weather Web: %.2f" %lapseRateW + " degrees C per km"
fitW = (mW*tWWW + bW)

mS, bS = pF.customLeastSquare(tSPC, aSPC)
lapseRateS = mS**-1
print "Lapse rate for SPC Great Falls sounding: %.2f" %lapseRateS + " degrees C per km"
fitS = (mS*tSPC + bS)

wx_new, wy_new, f1 = pF.polyFit(wAltitudes, wSpeeds, 3, len(wAltitudes))
dx_new, dy_new, f2 = pF.polyFit(wAltitudes, wDirections, 4, len(wAltitudes))

'''
For these, the fractional uncertainty in both x and y are generated
above to check whether they're on the same order of magnitude (Can't 
use linear least square fit) or not. Radiosonde data appears to
be pretty typically 4 orders of magnitude off.
'''

print "Fractional uncertainty in temperature sounding Graw: " + str(rX)
print "Fractional uncertainty in altitude sounding Graw: " + str(rY)

###########End best fit line section############



##############Plot data#########################

'''
Plotting values. Check the plotting.py code for more information
on these functions. Not much else to see, here.
'''
#Pre plot#
x, y = pF.convertVector(wSpeeds, wDirections)
fA = pF.deltaAFlattening(wAltitudes, deltaAltitude)
newX, newY, positionValue = pF.isolateDisc(lowerAltitude, upperAltitude, fA, wDirections, wSpeeds)
plotDict = pl.numPlots(13)
newLats, newLongs = pF.latLongDiff(lats, longs)
upperTrop = pF.upperTrop(f1, wx_new, 10)
print "Potential upper bound on tropopause: %.f" %upperTrop + " meters"

#Plotting#
'''
Wyoming weather web lapse rate. Uncomment to plot.
'''
#plotWWWLapse = pl.scatterAndFitLine(plotDict["ax0"], tWWW, aWWW, fitW, "Temperature", "Altitude", "Temperature vs. Altitude WWW", "Fit line")
'''
SPC sounding lapse rate. Uncomment to plot.
'''
#plotSPCLapse = pl.scatterAndFitLine(plotDict["ax1"], tSPC, aSPC, fitS, "Temperature", "Altitude", "Temperature vs. Altitude SPC", "Fit line")
'''
Graw sounding lapse rate. Uncomment to plot.
'''
#plotGrawLapse = pl.scatterAndFitLine(plotDict["ax2"], temperatures, altitudes, fitC, "Temperature", "Altitude", "Temperature vs. Altitude Graw", "Fit line", xErr=tUncertainty)
'''
3D plot of the u and v components of wind against altitude.
Uncomment to plot.
'''
#plotWinds3D = pl.threeDScatterPlot(plotDict["ax3"], x, y, fA, "U", "V", "Altitude")
'''
Polar plot of a section of U and V components of winds.
Uncomment to plot.
'''
#plotPolar = pl.polarPlot(plotDict["ax4"], newX, newY, "12000 to 14000 meters")
'''
Plot of altitude versus wind speeds with a polynomial best fit line.
Uncomment to plot.
'''
#plotAWs = pl.lineBestFit(plotDict["ax6"], wAltitudes, wSpeeds, wx_new, wy_new, "Altitudes", "Wind speeds", "Altitude vs. Wind speed")
'''
Altitude versus pressure plot. Uncomment to plot.
'''
#plotPA = pl.linePlot(plotDict["ax7"], pressures, wAltitudes, "Pressure", "Altitude", "Pressure vs. Altitude")
'''
Time versus altitude plot. Uncomment to plot.
'''
plotTA = pl.linePlot(plotDict["ax8"], time, wAltitudes, "Time", "Altitude", "Time vs. Altitude")
'''
Time versus pressure plot. Uncomment to plot.
'''
#plotTP = pl.linePlot(plotDict["ax9"], time, pressures, "Time", "Pressure", "Time vs. Pressure")
'''
Altitude versus wind direction plot, with a polynomial best fit line.
Uncomment to plot.
'''
#plotAWd = pl.lineBestFit(plotDict["ax10"], wAltitudes, wDirections, dx_new, dy_new, "Altitude", "Wind direction", "Altitude vs. Wind direction")
'''
Change in latitude vs. change in longitude vs. Altitude plot. 
Untested for validity. Uncomment to plot.
'''
#plotDLaDLoAlt = pl.threeDLinePlot(plotDict["ax11"], newLats[100:], newLongs[100:], wAltitudes[100:len(wAltitudes)-1], "delta Latitude", "delta Longitude", "Altitude")
'''
Latitude vs. Longitude vs. Altitude plot. Comparing against changes
in lat/long plot. Uncomment to plot.
'''
#plotLaLoAlt = pl.threeDLinePlot(plotDict["ax12"], lats[100:], longs[100:], wAltitudes[100:], "Latitudes", "Longitudes", "Altitudes")

##############End plot data#####################