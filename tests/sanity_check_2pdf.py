import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


from pluq.base import Correlation
from pluq.inbase import read_pdf, get_pdf, estimate_pdf
from pluq.dbtools import DBMySQL, PacsyCorrelation

if __name__ == "__main__":

    pacsy = DBMySQL(db='pacsy2', password='pass')

    corr1 = Correlation('V', ('CB', 'CA'), 'H')
    pacsy_corr = PacsyCorrelation(corr1, pacsy)
    data1 = pacsy_corr.get_cs(piqc=True, model=1, like_ss=False, sigma_n=10)
    smooth1 = estimate_pdf(data1, bandwidth=0.4)

    corr2 = Correlation('V', ('CB', 'CA'), 'C')
    pacsy_corr2 = PacsyCorrelation(corr2, pacsy)
    data2 = pacsy_corr2.get_cs(piqc=True, model=1, like_ss=False, sigma_n=10)
    smooth2 = estimate_pdf(data2, bandwidth=0.4)



    plt.figure(1)
    plt.hold(True)
    x, y = smooth1.grid
    z = smooth1.pdf
    plt.contour(x, y, z, list(smooth1.get_levels(data1, 94, 85, 68, 34, 5)), colors='r')

    x, y = smooth2.grid
    z = smooth2.pdf
    plt.contour(x, y, z, list(smooth2.get_levels(data1, 94, 85, 68, 34, 5)), colors='b')

    plt.xlim(35, 27)
    plt.ylim(75, 55)


    plt.show()