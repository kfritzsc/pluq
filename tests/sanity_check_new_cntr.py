from pluq.base import Correlation
from pluq.fileio import read_pdf
from pluq.inbase import get_pdf, _region

import matplotlib.pyplot as plt
from descartes import PolygonPatch


corr = Correlation('A', ('CB', 'CA'), ss='X')
pdf_dict = read_pdf('cc')
pdf = get_pdf(corr, pdf_dict)


fig = plt.figure()
ax = fig.add_subplot(111)

plt.imshow(pdf.pdf, interpolation="none", aspect='auto', origin='lower',
           extent=(pdf.limits[0][0], pdf.limits[0][1],
                   pdf.limits[1][0], pdf.limits[1][1]))

shapes = _region(pdf, pdf.levels[1])

for shape in shapes:
    patch = PolygonPatch(shape, fc='gray', ec='gray', alpha=0.5, zorder=1)
    ax.add_patch(patch)

plt.xlim([0, 100])
plt.ylim([0, 100])

plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.show()



print('Done')