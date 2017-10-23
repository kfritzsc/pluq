from pluq.base import CSExperiment, ProteinSeq
from pluq.dbtools import DBMySQL
from pluq.inbase import make_pdf, make_region

exp = CSExperiment(('C', 'H'), bonds=1)
pacsy = DBMySQL(db='pacsy_local', password='')



protein = ProteinSeq(None)
corrs = protein.relevant_correlations(exp, ignoresymmetry=True,
    offdiagonal=False)

file_name = 'ch_pdf_all.h5'
make_pdf(exp, pacsy, file_name)
#
#
# file_name = 'ch_region_all'
# make_region('ch', file_name, corrs)

#
# from pluq.fileio import read_pdf
#
# pdfs = read_pdf('ch')
#
# print(list(pdfs.keys()))
