import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


from pluq.base import Correlation
from pluq.inbase import load_pdf_dict, get_pdf, estimate_pdf
from pluq.dbtools import DBMySQL, PacsyCorrelation



if __name__ == "__main__":


    corr1 = Correlation('A', ('CA', 'CB'), 'H')
    corr2 = Correlation('A', ('CB', 'CA'), 'H')

    pacsy = DBMySQL(db='pacsy2', password='pass')
    pacsy_corr = PacsyCorrelation(corr1, pacsy)
    data1 = pacsy_corr.get_cs(piqc=True, model='all',  sigma_n=4, like_ss=True)

    data2 = pacsy_corr.get_cs(piqc=True, model='all',  sigma_n=4, like_ss=True)
    smooth1 = estimate_pdf(data1,
                          params={'bandwidth': np.linspace(0.4, 1.5, 15)})
    smooth2 = estimate_pdf(data2,
                          params={'bandwidth': np.linspace(0.4, 1.5, 15)})

    plt.figure(1)
    x, y = smooth1.grid
    z = smooth1.pdf
    plt.contour(x, y, z, list(smooth1.get_levels(data1, 68, 98, 95)))
    plt.figure(1)

    plt.figure(2)
    x, y = smooth1.grid
    z = smooth1.pdf
    plt.contour(x, y, z, list(smooth2.get_levels(data2, 68, 98, 95)))

    plt.show()