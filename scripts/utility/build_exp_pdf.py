from pluq.base import CSExperiment, ProteinSeq
from pluq.dbtools import DBMySQL
from pluq.inbase import make_pdf, make_region

exp = CSExperiment(('C', 'C'), bonds=1)
pacsy = DBMySQL(db='pacsy2', password='pass')
file_name = 'c_pdf_all'


protein = ProteinSeq(None)
corrs = protein.relevant_correlations(exp, ignoresymmetry=True, offdiagonal=False)


make_pdf(exp, pacsy, file_name)

# make_region('cc', file_name, corrs)