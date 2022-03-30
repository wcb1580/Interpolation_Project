# Earthquakes are sometimes associated with oil and gas production (taking mass out of the 
# ground) and injection (putting it back in) operations.
# 
# It has been suggested that injection of water at one particular site, which started midway through  
# 1993, has been responsible for a spate of recent earthquakes there. These are the data that were 
# plotted in the first exercise of sdlab_practice.py. The operator of the field has claimed they 
# cannot be responsible, because injection had been ongoing for almost 10 years before any earthquakes
# occurred.
#
# It has been proposed the earthquakes may be related to NET MASS CHANGES in the field. Therefore,
# it is necessary to understand how this quantity has evolved over time.
#
# Although data from the two production wells (mass extractors) - PW1 and PW2 - are reported regularly,
# data reporting from the injection well, IW1, is more irregular. In addition, the operator only 
# reports MASS RATES, not CUMULATIVE production or injection MASS.
import numpy as np
from numpy.linalg import norm, solve

from matplotlib import pyplot as plt
from sdlab_functions import *
#Import the data from the three data files
tm, pm1 = np.genfromtxt('PW1.dat', delimiter=',', skip_header=1).T
tq, pm2 = np.genfromtxt('PW2.dat', delimiter=',', skip_header=1).T
ty, iy = np.genfromtxt('IW1.dat', delimiter=',', skip_header=1).T
#obtain the years when two extraction sites both have data
years=np.intersect1d(tm,tq)
extraction=np.zeros((len(years)))
A=len(tm)
B=len(tq)
index=0
#Extraction rate without injection data
for i in range(A):
    for j in range(B):
        if tm[i]==tq[j]:
            extraction[index]=pm1[i]+pm2[j]
            index=index+1
#Calculate the coefficient for extraction
A=spline_coefficient_matrix(years)
b=spline_rhs(years,extraction)
C=solve(A,b)
# Estimate the extraction rate for years when injection data is given
extractionforinjectiontime=spline_interpolate(ty,years,C)
massrateforinjection=iy
#calculate the change of mass rate for years of injection
massrateforinjection=extractionforinjectiontime- massrateforinjection
#Calculate the mass rate changes for values in array years
A=spline_coefficient_matrix(ty)
b=spline_rhs(ty,massrateforinjection)
year=years[(years>=ty[0])*(years<= ty[-1])]#only obtains years that are in the interpolation range
ak=solve(A,b)
C=spline_interpolate(year,ty,ak)
#Obtain the actual change of mass rate
for i in range(len(years)):
    for j in range((len(year))):
        if years[i]==year[j]:
            extraction[i]=C[j]
A=spline_coefficient_matrix(ty)
b=spline_rhs(ty,iy)
c=solve(A,b)
Y=np.arange(ty[0],ty[-1],1)
injectionmassrate=spline_interpolate(year,ty,c)
# Injection mass changes
injectionchanges=np.zeros((len(year)-1))
for i in range(len(year)-1):
    injectionchanges[i]=((3600*365*(injectionmassrate[i+1]+injectionmassrate[i]))*(year[i+1]-year[i]))/2
# Calculate the mass changes
masschanges=np.zeros((len(years)-1))
for i in range(len(masschanges)):
    masschanges[i]=((3600*365*(extraction[i+1]+extraction[i]))*(years[i+1]-years[i]))/2
A=spline_coefficient_matrix(years[1:])
b=spline_rhs(years[1:],masschanges)
c=solve(A,b)
#plot the graph for Mass changes versus time
f, ax1 = plt.subplots(1, 1)
ax2 = ax1.twinx()
ax2.set_ylim([0, max(injectionchanges)+2*10**6])
ax2.set_ylabel('injection mass changes(1:1*10^7 kg)')
ax2.plot(year[1:], injectionchanges, 'b--',label='injection mass change', markersize=6)
ax1.arrow(2003.5, 15, 0., -100000, length_includes_head=True, head_width=0.2, head_length=0.1, color='b')
ax1.text(2003., 14.65, 'M 3.5', ha='right', va='center', size=10, color='b')
ax1.arrow(2004.5, 15, 0., -100000, length_includes_head=True, head_width=0.2, head_length=0.1, color='b')
ax1.text(2004.5, 15.2, 'M 4.0', ha='center', va='bottom', size=10, color='b')
ax1.arrow(2005., 15, 0., -100000, length_includes_head=True, head_width=0.2, head_length=0.1, color='b')
ax1.text(2005.5, 14.65, 'M 4.3', ha='left', va='center', size=10, color='b')
ax1.plot(ty[1:], spline_interpolate(ty[1:],years[1:],c), 'ko', label='injection time', zorder=2)
ax1.plot(years[1:],masschanges,'r-',label='Change of Mass',zorder=2)
ax1.legend(loc=3)
ax2.legend(loc=4)
ax1.set_xlabel('time(years)')
ax1.set_ylabel('Mass changes(1:1*10^6 kg)')
ax1.set_title('Mass changes vs time in relation to the earthquake')
save_figure = False
if not save_figure:
        plt.show()
else:
        plt.savefig('lab3_plot.png', dpi=300)


























