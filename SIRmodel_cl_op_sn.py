
from numba import njit, prange
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches

p = 1														#population
i = 0.01*p  												#infected
s = p-i														#susceptible
r = 0														#recovered/removed

a = 3.2														#transmission parameter
b = 0.23													#recovery parameter

initialTime = 0
deltaTime = 0.001											#smaller the delta, better the approximation to a real derivative
maxTime = 10000												#more number of points, better is the curve generated

@njit(nogil=True)
def sPrime(oldS, oldI, transmissionRate):					#differential equations being expressed as functions to
	return -1*((transmissionRate*oldS*oldI)/p)				#calculate rate of change between time intervals of the
	
@njit(nogil=True)															#different quantities i.e susceptible, infected and recovered/removed
def iPrime(oldS, oldI, transmissionRate, recoveryRate):				
	return (((transmissionRate*oldS)/p)-recoveryRate)*oldI

@njit(nogil=True)
def rPrime(oldI, recoveryRate):
	return recoveryRate*oldI

maxTimeInitial = maxTime

@njit(nogil=True, parallel=True)
def genData(transRate, recovRate, maxT):
	sInitial = s
	iInitial = i
	rInitial = r

	time = np.arange(maxT+1)
	sVals = np.zeros(maxT+1)
	iVals = np.zeros(maxT+1)
	rVals = np.zeros(maxT+1)

	for t in prange(initialTime, maxT+1):						#generating the data through a loop
		sVals[t] = sInitial
		iVals[t] = iInitial
		rVals[t] = rInitial

		newDeltas = (sPrime(sInitial, iInitial, transmissionRate=transRate), iPrime(sInitial, iInitial, transmissionRate=transRate, recoveryRate=recovRate), rPrime(iInitial, recoveryRate=recovRate))
		sInitial += newDeltas[0]*deltaTime
		iInitial += newDeltas[1]*deltaTime
		rInitial += newDeltas[2]*deltaTime

		if sInitial < 0 or iInitial < 0 or rInitial < 0:		#as soon as any of these value become negative, the data generated becomes invalid
			break												#according to the SIR model, we assume all values of S, I and R are always positive.

	return (time, sVals, iVals, rVals)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.4, top=0.94)

plt.title('SIR epidemiology curves for a disease')

plt.xlim(0, maxTime+1)
plt.ylim(0, p*1.4)

plt.xlabel('Time (t)')
plt.ylabel('Population (p)')

initialData = genData(a, b, maxTimeInitial)

susceptible, = ax.plot(initialData[0], initialData[1], label='Susceptible', color='b')
infected, = ax.plot(initialData[0], initialData[2], label='Infected', color='r')
recovered, = ax.plot(initialData[0], initialData[3], label='Recovered/Removed', color='g')

plt.legend()

transmissionAxes = plt.axes([0.125, 0.25, 0.775, 0.03], facecolor='white')
recoveryAxes = plt.axes([0.125, 0.2, 0.775, 0.03], facecolor='white')
timeAxes = plt.axes([0.125, 0.15, 0.775, 0.03], facecolor='white')

transmissionSlider = Slider(transmissionAxes, 'Transmission parameter', 0, 10, valinit=a, valstep=0.01)
recoverySlider = Slider(recoveryAxes, 'Recovery parameter', 0, 10, valinit=b, valstep=0.01)
timeSlider = Slider(timeAxes, 'Max time', 0, 100000, valinit=maxTime, valstep=1, valfmt="%i")

def updateTransmission(newVal):
	global a
	a = newVal

	newData = genData(newVal, b, maxTimeInitial)

	susceptible.set_ydata(newData[1])
	infected.set_ydata(newData[2])
	recovered.set_ydata(newData[3])

	r_o.set_text(r'$R_O$={:.2f}'.format(a/b))

	fig.canvas.draw_idle()

def updateRecovery(newVal):
	global b
	b = newVal

	newData = genData(a, newVal, maxTimeInitial)

	susceptible.set_ydata(newData[1])
	infected.set_ydata(newData[2])
	recovered.set_ydata(newData[3])

	r_o.set_text(r'$R_O$={:.2f}'.format(a/b))

	fig.canvas.draw_idle()

def updateMaxTime(newVal):
	global susceptible, infected, recovered, maxTimeInitial
	maxTimeInitial = int(newVal.item())

	newData = genData(a, b, int(newVal.item()))

	del ax.lines[:3]

	susceptible, = ax.plot(newData[0], newData[1], label='Susceptible', color='b')
	infected, = ax.plot(newData[0], newData[2], label='Infected', color='r')
	recovered, = ax.plot(newData[0], newData[3], label='Recovered/Removed', color='g')

transmissionSlider.on_changed(updateTransmission)
recoverySlider.on_changed(updateRecovery)
timeSlider.on_changed(updateMaxTime)

resetAxes = plt.axes([0.8, 0.025, 0.1, 0.05])
resetButton = Button(resetAxes, 'Reset', color='white')

r_o = plt.text(0.1, 1.5, r'$R_O$={:.2f}'.format(a/b), fontsize=12)

def reset(event):
    transmissionSlider.reset()
    recoverySlider.reset()
    timeSlider.reset()

resetButton.on_clicked(reset)

plt.show()
