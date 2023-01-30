from scipy.signal import chirp, find_peaks, peak_widths
import matplotlib.pyplot as plt
import numpy as np

#thx to
#https://stackoverflow.com/questions/71394572/scipy-signal-peak-widths-not-evaluating-at-correct-index
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.peak_widths.html

def fwhm_and_plot(mccode_data,monitor):
    size_mccode_data=len(mccode_data)
    X_mcxtrace = np.zeros(size_mccode_data)
    Y_mcxtrace = np.zeros(size_mccode_data)

    i=0
    for elt in mccode_data:
        X_mcxtrace[i] = elt[0]
        Y_mcxtrace[i] = elt[monitor]
        #print(X_mcxtrace[i],Y_mcxtrace[i])
        i+=1

    max_Y_mcxtrace = max(Y_mcxtrace)
    i=0
    for elt in mccode_data:
        Y_mcxtrace[i] = Y_mcxtrace[i]/max_Y_mcxtrace
        i+=1
    max_X_mcxtrace = max(X_mcxtrace)

    x = np.array(X_mcxtrace)
    y = np.array(Y_mcxtrace)

    peaks, _ = find_peaks(y)
    results_half = peak_widths(y, peaks, rel_height=0.5)


    b=((((results_half[2])/(y.size-1))-0.5)*2)*max_X_mcxtrace
    c=((((results_half[3])/(y.size-1))-0.5)*2)*max_X_mcxtrace

    print("fwhm: ",c-b)

    plt.plot(x,y)
    plt.plot(x[peaks], y[peaks], "x")
    plt.hlines(results_half[1], b,c,color="C2")
    plt.show()




