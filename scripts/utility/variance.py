
from pluq.dbtools import DBMySQL
from pluq.aminoacids import aa_list, aa_atoms

pacsy = DBMySQL(db='pacsy_local', password='')


cs_vars = []
for aa in aa_list:
    for atom in aa_atoms[aa]:
        sql = "SELECT std(C_SHIFT) FROM {}_CS_DB WHERE ATOM_NAME Like '{}'".format(aa, atom)
        try:
            result = float(pacsy.query(sql)[0][0])**2
            cs_vars.append([aa, atom, result])
        except:
            pass

# import pandas as pd
# df = pd.DataFrame(cs_vars, columns=['Res', 'Atom', 'Var'])
# df.to_csv('cs_vars.csv')


