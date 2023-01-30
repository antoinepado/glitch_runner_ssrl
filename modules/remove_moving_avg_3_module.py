import numpy as np
import matplotlib.pyplot as plt

########### Get data from digitalized_data.txt, the digitalized ssrl db data
data_ssrl = np.loadtxt("./data/digitalized_ssrl_data/digitalized_data.txt", encoding='utf-8-sig',delimiter=";")
size_data_ssrl = len(data_ssrl)
X_ssrl = np.zeros(size_data_ssrl)
Y_ssrl = np.zeros(size_data_ssrl)

i=0
for elt in data_ssrl:    
    X_ssrl[i] = 1000.0*elt[0]
    Y_ssrl[i] = elt[1]
    i+=1

########### Get data from theory_itsty_firstxtal.dat, the theory glitches
data_theory_glitches = np.loadtxt("./data/data_from_theory_glitches/theory_itsty_firstxtal.dat")
size_data_theory_glitches = len(data_theory_glitches)
X_theory_glitches = np.zeros(size_data_theory_glitches)
Y_theory_glitches = np.zeros(size_data_theory_glitches)
i=0
for elt in data_theory_glitches:
    X_theory_glitches[i] = elt[0]
    #relative intensities are of interest.
    Y_theory_glitches[i] = -elt[1]*(30.69/71350.83)
    i+=1
           
########### Get data from McXtrace's mccode.dat
screen=1
data_mcxtrace = np.loadtxt("./data/data_mcxtrace/1_ev_src/mccode.dat")
size_data_mcxtrace = len(data_mcxtrace)
X_mcxtrace = np.zeros(size_data_mcxtrace)
Y_mcxtrace = np.zeros(size_data_mcxtrace)
Y_mcxtrace_nan = np.zeros(size_data_mcxtrace)
#what is above the threshold isn't a glitch
#what is under is
threshold = 0.999 #0.999
not_in_glitch = 1
i=0
for elt in data_mcxtrace:    
    X_mcxtrace[i]=elt[0]
    Y_mcxtrace[i]=elt[screen]
    Y_mcxtrace_nan[i]=elt[screen]
    i+=1
      
max_Y_mcxtrace = max(Y_mcxtrace)    
 
########### Get rid of glitches, detect where they are and nan the portions, then replace the nans by interpolation       
i=0
for elt in data_mcxtrace:
    if i!=0 and i!=(size_data_mcxtrace-1):
      y_diff_sign = Y_mcxtrace[i]-Y_mcxtrace[i-1]
      if y_diff_sign<0:
        y_diff_sign = -1
        y_div = Y_mcxtrace[i]/Y_mcxtrace[i-1]
      else:
        y_diff_sign = 1
        y_div = Y_mcxtrace[i-1]/Y_mcxtrace[i]
        
      y_diff = np.abs(Y_mcxtrace[i]-Y_mcxtrace[i-1])
            
      if not_in_glitch==1:
        if y_div<threshold:
          not_in_glitch = 0          
      elif not_in_glitch==0: 
        if y_div>threshold:
          if(y_diff_sign>=1):
            if((Y_mcxtrace[i]/Y_mcxtrace[i+1])>threshold): #also the point after it
              not_in_glitch=1
          
      if not_in_glitch==0:
        Y_mcxtrace_nan[i] = np.nan
        
    i+=1    
    
not_nan = np.logical_not(np.isnan(Y_mcxtrace_nan))
indices = np.arange(len(Y_mcxtrace_nan))
without_glitches = np.interp(indices, indices[not_nan], Y_mcxtrace_nan[not_nan])
max_without_glitches = max(without_glitches)

for i,elt in enumerate(without_glitches):
    without_glitches[i]=(without_glitches[i]/max_without_glitches)*100

for i,elt in enumerate(Y_mcxtrace):
    Y_mcxtrace[i]=(Y_mcxtrace[i]/max_Y_mcxtrace)*100

#moving avg
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w
    
#window length of the moving avg
nn=100#6000
o = moving_average(without_glitches, nn)
y_padded = np.pad(o, (nn//2, nn-1-nn//2), mode='edge')
#print("shape",y_padded.shape,without_glitches.shape)

#Look at the normal plot and the plot without the glitches
#Check that it is correct before looking at the plot of Y_mcxtrace 
#plt.plot(X_mcxtrace, Y_mcxtrace, marker='x', color="r")
#plt.plot(X_mcxtrace, y_padded,marker='x', color="g")

#take off the moving avg without the glitches from the original plot with glitches
for i,elt in enumerate(Y_mcxtrace):
    Y_mcxtrace[i]=Y_mcxtrace[i]-y_padded[i]

#optional, you can try to bring a glitch to the same intensity as one of the ssrl glitches to see if the other glitches fit
for i,elt in enumerate(Y_mcxtrace):
    Y_mcxtrace[i]=Y_mcxtrace[i]*(30.69/94.91)

plt.title("Intensity deviation. Si 220 phi 90.")
plt.xlabel("E")
plt.ylabel("I deviation")
plt.plot(X_theory_glitches, Y_theory_glitches, marker='x', color="y", label='theory')
plt.plot(X_ssrl, Y_ssrl, marker='.', color="r", label='main db ssrl-db BL11-2')
plt.plot(X_mcxtrace, Y_mcxtrace, marker='.', color="g", label='McXtrace')
plt.legend(fontsize=10)
plt.show()
