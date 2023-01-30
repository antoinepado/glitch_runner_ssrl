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
    #relative intensities are of interest, give the same intensity deviation to the theory glitch as the most intense ssrl glitch
    Y_theory_glitches[i] = -elt[1]*(30.69/71350.83)
    i+=1

########### Get data from McXtrace's mccode.dat
def mccode_values(filename,nn):
    data_mcxtrace=np.loadtxt("./data/data_mcxtrace/white_source/energy_scan/"+filename)
    size_data_mcxtrace=len(data_mcxtrace)
    X_mcxtrace = np.zeros(size_data_mcxtrace)
    Y_mcxtrace = np.zeros(size_data_mcxtrace)

    i=0
    for elt in data_mcxtrace:    
        X_mcxtrace[i]=elt[0]
        Y_mcxtrace[i]=elt[1]
        i+=1
          
    max_Y_mcxtrace = max(Y_mcxtrace)    
    for i,elt in enumerate(Y_mcxtrace):
        Y_mcxtrace[i]=(Y_mcxtrace[i]/max_Y_mcxtrace)*100

    #moving avg
    def moving_average(x, w):
        return np.convolve(x, np.ones(w), 'valid') / w
        
    #window length of the moving avg
    o = moving_average(Y_mcxtrace, nn)
    y_padded = np.pad(o, (nn//2, nn-1-nn//2), mode='edge')

    #Look at the normal plot and the plot without the glitches
    #Check that it is correct before looking at the plot of Y_mcxtrace 
    #plt.plot(X_mcxtrace, Y_mcxtrace,marker='x', color="r")
    #plt.plot(X_mcxtrace, y_padded,marker='x', color="g")

    #take off the moving avg without the glitches from the original plot with glitches
    for i,elt in enumerate(Y_mcxtrace):
        Y_mcxtrace[i]=Y_mcxtrace[i]-y_padded[i]
    
    #relative intensities are of interest, give the same intensity deviation to the mcxtrace glitch as the most intense ssrl glitch    
    for i,elt in enumerate(Y_mcxtrace):
        Y_mcxtrace[i]=Y_mcxtrace[i]*(30.69/64.2)     
    
    return X_mcxtrace,Y_mcxtrace 

list_Y_mcxtrace = []
X_mcxtrace = []
Y_mcxtrace = []
moving_window_numberofpoints_list = [50,300,300,500,400,600,300,300,500,400,500,600,800,700,800,800,1500]

ii = 0
for egy in range(4500,20500,1000):
    filename="mccode_"+str(egy)+"_"+str(egy+1000)+".dat"
    X_mcxtrace, Y_mcxtrace = mccode_values(filename,moving_window_numberofpoints_list[ii])
    list_Y_mcxtrace.append(list(Y_mcxtrace))
    ii+=1

X_mcxtrace, Y_mcxtrace = mccode_values("mccode_20500_27000.dat",moving_window_numberofpoints_list[ii])
list_Y_mcxtrace.append(list(Y_mcxtrace))

plt.title("Intensity deviation. Si 220 phi 90.")
plt.xlabel("E")
plt.ylabel("I deviation")
plt.plot(X_theory_glitches, Y_theory_glitches, marker='x', color="y", label='theory')
plt.plot(X_ssrl, Y_ssrl, marker='.', color="r", label='main db ssrl-db BL11-2')

concatenated_X_mcxtrace = []
concatenated_Y_mcxtrace = []
for elt_Y in list_Y_mcxtrace:
    concatenated_Y_mcxtrace+=elt_Y
    
ii=4500
while ii<=27000:
    ii+=1
    concatenated_X_mcxtrace.append(ii)

plt.plot(concatenated_X_mcxtrace, concatenated_Y_mcxtrace, marker='.',color="g", label='McXtrace')
plt.legend(fontsize=10)
plt.show()
