# -*- coding: utf-8 -*-
"""
This program imports data from the file specified by the string filename
The first line of the file is ignored (assuming it's the name of the variables)
After that the data file needs to be formatted: 
number space number space number space number newline
Do NOT put commas in your data file!!
The data file should be in the same directory as this python file
The data should be in the order:
x_data y_data x_uncertainty y_uncertainty

Then this program tries to fit a function to the data points
It plots the data as dots with errorbars and the best fit line
It then prints the best fit information
After that, it plots the "residuals": ydata - fittedfunction(xdata)
That is it subtracts your fitted ideal values from your actual data to see 
what is "left over" from the fit
Ideally your residuals graph should look like noise, otherwise there is more
information you could extract from your data (or you used the wrong fitting
function)

If you want to change the graph labels, look for the plt.xlabel() commands
If you want to change the file name, that's the next line below this comment
"""
filename="data.txt"
# change this if your filename is different


import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from pylab import loadtxt


data=loadtxt(filename, usecols=(0,1), skiprows=1, unpack=True)
# load filename, take columns 0 & 1 & 2 & 3, skip 1 row, unpack=transpose x&y

xdata=data[0][:200]
ydata=data[1][:200]

# finished importing data, naming it sensibly

def my_func(t,a,tau,T,phi):
    return a*np.exp(-t/tau)*np.cos(2*np.pi*t/T+phi)
# this is the function we want to fit. the first variable must be the
# x-data (time), the rest are the unknown constants we want to determine

popt, pcov = optimize.curve_fit(my_func, xdata, ydata)
# we have the best fit values in popt[], while pcov[] tells us the uncertainties

a=popt[0]
tau=popt[1]
T=popt[2]
phi=popt[3]
# best fit values are named nicely
u_a=pcov[0,0]**(0.5)
u_tau=pcov[1,1]**(0.5)
u_T=pcov[2,2]**(0.5)
u_phi=pcov[3,3]**(0.5)
print(pcov)
# uncertainties of fit are named nicely

# def fitfunction(t):  
#     return a*np.exp(-t/tau)*np.cos(2*np.pi*t/T+phi)
# #fitfunction(t) gives you your ideal fitted function, i.e. the line of best fit

# start=min(xdata)
# stop=max(xdata)    
# xs=np.arange(start,stop,(stop-start)/1000) # fit line has 1000 points
# curve=fitfunction(xs)
# # (xs,curve) is the line of best fit for the data in (xdata,ydata) 

# plt.rcParams["figure.figsize"] = (10,6)
# # Change the size of your plot - numbers are inches because USA

# plt.errorbar(xdata,ydata,yerr=yerror,xerr=xerror,fmt=".")
# # plot the data, fmt makes it data points not a line
# plt.plot(xs,curve)
# # plot the best fit curve on top of the data points as a line

# plt.xlabel("xdata")
# plt.ylabel("ydata")
# plt.title("Best fit of some data points")
# # HERE is where you change how your graph is labelled!

# plt.show()
# # show the graph


# print("A:", a, "+/-", u_a)
# print("tau:", tau, "+/-", u_tau)
# print("T:", T, "+/-", u_T)
# print("phi:", phi, "+/-", u_phi)
# # prints the various values with uncertainties

# plt.rcParams["figure.figsize"] = (10,3)
# # Change the size of your plot - numbers are inches because USA

# residual=ydata-fitfunction(xdata)
# # find the residuals
# zeroliney=[0,0]
# zerolinex=[start,stop]
# # create the line y=0

# plt.errorbar(xdata,residual,yerr=yerror,xerr=xerror,fmt=".")
# # plot the residuals with error bars
# plt.plot(zerolinex,zeroliney)
# # plotnthe y=0 line on top

# plt.xlabel("xdata")
# plt.ylabel("residuals of ydata")
# plt.title("Residuals of the fit")
# # HERE is where you change how your graph is labelled!

# plt.show()
# # show the graph