"""
Classes for getting data from the PACSY database.

"""

import numpy as np
import pluq.aminoacids as aminoacids
from pluq.base import Correlation, ProteinSeq

try:
    import MySQLdb

except:
    try:
        import mysqlclient as MySQLdb
    except:
        msg= 'MySQLdb-Python or mysqlclient must be installed!'
        raise ImportError(msg)


class DBMySQL(object):
    """
    Small "wrapper class" for working with MySQLdb. Especially useful
    if multiple database connections must be open at the same time.
    All operation are wrapped in exceptions.

    :param host: hostname like 'localhost'
    :param user: username like 'root'
    :param password: password like 'pass'
    :param db: database name like pacsy
    """

    # TODO: Wrap MySQL errors better.
    def __init__(self, host='localhost', user='root', password='',
                 db='pacsy'):
        try:
            self.connection = MySQLdb.connect(host, user, password, db)
            self.cursor = self.connection.cursor()
            self.dict_cursor = self.connection.cursor(
                MySQLdb.cursors.DictCursor)
            self.db = db
        except MySQLdb.Error as e:
            try:
                print("MySQL Error {}: {}".format(e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error: {}".format(str(e)))

    def query(self, query, dict_cursor=False):
        """Query the database and return.
        :param query: sql string
        :param dict_cursor: bool, False for list return, True for a dict
        """
        try:
            if dict_cursor:
                self.dict_cursor.execute(query)
                results = self.dict_cursor.fetchall()
            else:
                self.cursor.execute(query)
                results = self.cursor.fetchall()
            return results
        except MySQLdb.Error as e:
            self.connection.rollback()
            try:
                print("MySQL Error {}: {}".format(e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error: {}".format(str(e)))

    def insert(self, query):
        """Use query to insert and the commit to the database.
        :param query: sql string
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()

        except MySQLdb.Error as e:
            self.connection.rollback()
            try:
                print("MySQL Error {}: {}".format(e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error: {}".format(str(e)))

    def table_exist(self, name):
        """ Returns True if the database contains a table with the given name.

        :param name: str, name of table
        """
        sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{}'
        AND table_name = '{}'""".format(self.db, name)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                return False

        except MySQLdb.Error as e:
            self.connection.rollback()
            try:
                print("MySQL Error {}: {}".format(e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error: {}".format(str(e)))

    def bulk_inset(self, query):
        """
        Use query to insert. You must commit manually!!! This is useful when
        you are inserting data from a loop, etc..

        :param query: sql string
        """
        try:
            self.cursor.execute(query)

        except MySQLdb.Error as e:
            self.connection.rollback()
            try:
                print("MySQL Error {}: {}".format(e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error: {}".format(str(e)))

    def commit(self):
        """ Commit the data to the database"""
        try:
            self.connection.commit()
        except MySQLdb.Error as e:
            self.connection.rollback()
            try:
                print("MySQL Error {}: {}".format(e.args[0], e.args[1]))
            except IndexError:
                print("MySQL Error: {}".format(str(e)))

    def __del__(self):
        self.connection.close()

    def __str__(self):
        self.db


class PacsyCorrelation(object):
    """
    Class for finding data for a specific correlation in the PACSY database.
    Queries are added as methods.

    :param correlation: pluq.base.Correlation
    :param database: pluq.dbtools.DBMySQL
    """

    def __init__(self, correlation, database):
        self.correlation = correlation
        self.database = database
        self.dims = len(correlation.atoms)

    def get_cs(self, model=1, limits=None, prev_aa=None, next_aa=None,
               piqc=False, sigma_n=None, like_ss=True, debug=False):
        """
        Get the chemical shifts of an intra-residue correlation. Optionally
        limit the range of the chemical shifts, specify what model number to
        use (for secondary- structure), limit the results by the preceding
        and/or next residue in the sequence, limit by PIQC analysis, etc.

        :param limits: chemical shift limits in the format,
                       default [[-inf, inf], ] * n
                       [(cs1_min, cs2_max),...(csn_min, csn_max)]
        :param model:  secondary-structure check to 'most' models, 'all' models
                       or specific model. If 'all' each model must have the
                       same snd_stc. If 'most' most models must have the same
                       snd_stc.
        :param prev_aa: 1-letter amino acid code of acceptable previous amino-
                        acids in the sequence, None == any
                        str or list of str
        :param next_aa: 1-letter amino acid code of acceptable previous amino-
                        acids in the sequence, None == any
                        str or list of str
        :param piqc: limit to proteins that are satisfy PIQC
        :param sigma_n: prune chemical shifts > sigma_n * std from the average
        :param like_ss: if True groups ss into similar categories
                        see aminoacids.common_sndstr for details of grouping
        :param debug: prints out sql statement
        :return: [(cs1_1, cs2_2, ... csn_n),.. (csm_1, csm_2, ... csm_n) ]
        """

        # Validate input.
        aa = self.correlation.aa
        if aa not in aminoacids.aa_list:
                mesg = '{} is not a supported amino-acid!'.format(aa)
                raise ValueError(mesg)

        for atom in self.correlation.atoms:
            if atom not in aminoacids.aa_atoms[aa]:
                raise ValueError('{} is not an atom in {}'.format(atom, aa))
        if prev_aa:
            prev_aa = tuple(set(prev_aa))
            for prev_aa_i in prev_aa:
                if prev_aa_i not in aminoacids.aa_list:
                    mesg = '{} is not an amino-acid!'.format(prev_aa_i)
                    raise ValueError(mesg)
        if next_aa:
            next_aa = tuple(set(next_aa))
            for next_aa_i in next_aa:
                if next_aa_i not in aminoacids.aa_list:
                    mesg = '{} is not an amino-acid!'.format(next_aa_i)
                    raise ValueError(mesg)

        if piqc and not self.database.table_exist('SEQ_CS_DB'):
            mesg = 'The PIQC table is not in {}.'.format(self.database)
            raise ValueError(mesg)

        ss = self.correlation.ss
        n = self.dims

        # Scary sub-query to find unique secondary structure or the most common
        # secondary structure. I am sorry ...
        if model == 'all':
            sub_sql = """INNER JOIN(
            SELECT DISTINCT c.KEY_ID, c.SND_STRC  FROM {0}_strc_db as c
            INNER JOIN (
            SELECT KEY_ID, COUNT(a.KEY_ID) as count FROM (
            SELECT DISTINCT KEY_ID, SND_STRC FROM {0}_strc_db
            GROUP BY KEY_ID, SND_STRC)as a
            GROUP BY KEY_ID
            HAVING count = 1
            ) as b ON c.KEY_ID = b.KEY_ID ) as strc
            ON cs_0.KEY_ID = strc.KEY_ID""".format(aa)

        if model == 'most':
            sub_sql = """INNER JOIN (SELECT  KEY_ID,
            SUBSTRING_INDEX(GROUP_CONCAT(x.SND_STRC
            ORDER BY x.count DESC SEPARATOR ':::'), ':::', 1) AS snd_strc_mode
            FROM (SELECT KEY_ID, SND_STRC, COUNT(*) as count FROM {0}_strc_db
            GROUP BY KEY_ID, SND_STRC) as x
            GROUP BY x.KEY_ID ) as xx
            ON cs_0.KEY_ID = xx.KEY_ID""".format(aa)

        # Build SQL query
        # Select Chemical Shifts From Sub Table(s)
        cs = 'cs_{0}.C_SHIFT as cs{0}'
        sql = [("SELECT " + ', '.join([cs.format(x) for x in range(n)])),
               "FROM {0}_cs_db as cs_0".format(aa)]

        # Join other sub table for chemical shift.
        for ni in range(1, n):
            sql.append("INNER JOIN {0}_cs_db AS cs_{1} ".format(aa, ni))
            sql.append("ON cs_0.KEY_ID = cs_{0}.KEY_ID".format(ni))

        # Join other sub table for structure
        if ss and ss != 'X':
            if model in {'all', 'most'}:
                sql.append(sub_sql)
            else:
                sql.append("INNER JOIN {0}_strc_db AS strc".format(aa))
                sql.append("ON cs_0.KEY_ID = strc.KEY_ID")

        if prev_aa or next_aa:
            sql.append("INNER JOIN {0}_db AS info".format(aa))
            sql.append("ON cs_0.KEY_ID = info.KEY_ID")

        if piqc:
            sql.append("INNER JOIN SEQ_CS_DB ")
            sql.append("ON cs_0.FIRSTKEY_ID = SEQ_CS_DB.KEY_ID")

        # Start of the where statements.
        # Atoms and Limits for first atom
        atom_0 = self.correlation.atoms[0]
        sql.append("WHERE cs_0.ATOM_NAME = '{0}'".format(atom_0))

        if prev_aa:
            if len(prev_aa) == 1:
                sql.append("AND info.PREV_X = '{}'".format(prev_aa[0]))
            else:
                sql.append("AND info.PREV_X in {}".format(prev_aa))

        if next_aa:
            if len(next_aa) == 1:
                sql.append("AND info.NEXT_X = '{}'".format(next_aa[0]))
            else:
                sql.append("AND info.NEXT_X in {}".format(next_aa))

        if limits:
            sql.append("AND cs_0.C_SHIFT")
            limits_0 = (limits[0][0], limits[0][1])
            sql.append("BETWEEN {0} AND {1}".format(limits_0))

        # Atoms and Limits for rest of the atom
        for ni in list(range(1, n)):
            sql.append("AND cs_{0}.ATOM_NAME = '{1}'".format(
                ni, self.correlation.atoms[ni]))

            if limits:
                sql.append("AND cs_{0}.C_SHIFT ".format(ni))
                limits_n = (limits[ni][0], limits[ni][1])
                sql.append("BETWEEN {0} AND {1}".format(limits_n))

        # If secondary structure
        if ss and ss != 'X':
            try:
                ss_list = aminoacids.similar_sndstr[ss]
            except KeyError:
                raise ValueError('{} is not a valid sndstr'.format(ss))

            if model == 'all':
                if like_ss:
                    sql.append("AND strc.SND_STRC IN {0}".format(ss_list))
                else:
                    sql.append("AND strc.SND_STRC = '{}'".format(ss))
            elif model == 'most':
                if like_ss:
                    sql.append("AND xx.snd_strc_mode IN {0}".format(ss_list))
                else:
                    sql.append("AND xx.snd_strc_mode = '{0}'".format(ss))
            else:
                if like_ss:
                    sql.append("AND SND_STRC IN {0}".format(ss_list))
                else:
                    sql.append("AND SND_STRC = '{0}'".format(ss))
                sql.append("AND MODEL_NO={0}".format(model))

        if piqc:
            sql.append("AND ELEMENT='C'")
            sql.append("AND PIQC = 1")

        sql = [x.strip() for x in sql]
        sql = '\n'.join(sql)

        if debug:
            print(sql)

        cs = self.database.query(sql)

        if not cs:
            raise ValueError

        if sigma_n:
            avg = np.mean(cs, axis=0)
            std = np.std(cs, axis=0)
            ind = np.all(np.abs(cs-avg) <= std*sigma_n, axis=1)
            cs = np.compress(ind, cs, axis=0)

        return cs

    def get_rama(self, limits=None, models=None, debug=False):
        """
        Get the Phi, Psi, dihedral angles of a correlation. Optionally find
        correlation within chemical shift limits or specify what model numbers
        to include.

        :param limits: chemical shift limits in the format,
                       default [[-inf, inf], ] * n
                       [(cs1_min, cs2_max),... (csn_min, csn_max)]
        :param models: limit to some models by model number identifier
                       number or [number1, number2, ...number_n], default all
        :param debug: print sql statement
        :return: [(phi_1, psi_1), (phi_2, psi_2), (phi_m, psi_m), ]
        """

        res = self.correlation.aa
        ss = self.correlation.ss

        # First Atom
        sql = """
        SELECT Structure.PHI, Structure.PSI
        FROM (
        SELECT KEY_ID, C_SHIFT
        FROM   {0}_cs_db
        WHERE  ATOM_NAME = '{1}'""".format(res, self.correlation.atoms[0])

        if not limits:
            sql += ") cs0"
        else:
            sql += """
            AND C_SHIFT BETWEEN   {0} AND  {1}
            ) cs0""".format(limits[0][0], limits[0][1])

        # The Rest of the Atoms.
        for n in range(1, self.dims):
            sql += """
            JOIN (
            SELECT KEY_ID, C_SHIFT
            FROM   {0}_cs_db
            WHERE ATOM_NAME = '{1}'""".format(res, self.correlation.atoms[n])
            if not limits:
                sql += ") cs{} USING (KEY_ID)".format(n)
            else:
                sql += """
                AND  C_shift BETWEEN {0} AND {1}
                ) cs{2} USING (KEY_ID)""".format(limits[n][0], limits[n][1], n)

        # Optionally limit by Secondary-structure
        if not ss or ss == 'X':
            sql += """
            JOIN (
            SELECT KEY_ID, PHI, PSI
            FROM   {0}_strc_db
            WHERE PHI IS NOT NULL
            AND PSI IS NOT NULL""" .format(res)
        else:
            sql += """
            JOIN (
            SELECT KEY_ID, SND_STRC, PHI, PSI
            FROM   {0}_strc_db
            WHERE SND_STRC = '{1}'
            AND PHI IS NOT NULL
            AND PSI IS NOT NULL""".format(res, ss)

        # Optionally limit the included models.
        try:
            models = list(iter(models))
            models = map(int, models)
            try:
                join_models = ', '.join(map(str, models))
                sql += 'AND MODEL_NO in ({})'.format(join_models)
            except ValueError:
                raise

        except TypeError:
            try:
                models = int(models)
                sql += 'AND MODEL_NO = {}'.format(models)
            except TypeError:
                pass
            except ValueError:
                raise

        sql += ') Structure USING (KEY_ID)'

        if debug:
            print(sql)

        return self.database.query(sql)


class PacsyProtein(object):
    """
    Class for working with an individual protein in the PACSY database.
    Queries are used to get properties and are added as methods.

    :param protein_id: pluq.base.ProteinID
    :param database: pluq.dbtools.DBMySQL
    """

    def __init__(self, protein_id, database):
        self.protein_id = protein_id
        self.database = database


    @property
    def id_dict(self):
        all_id = {}
        for new_idtype in {'ID', 'KEY_ID', 'BMRB_ID', 'PDB_ID'}:
            sql = "SELECT {} FROM seq_db WHERE {} = {}". \
                format(new_idtype, self.protein_id.idtype, self.protein_id.id)
            id_value = self.database.query(sql)

            if not id_value:
                mesg = "{}: {} is not a protein in the database.".format(
                    self.protein_id.idtype, self.protein_id.id)
                raise ValueError(mesg)

            id_value = id_value[0][0]
            if new_idtype in {'ID', 'KEY_ID', 'BMRB_ID'}:
                id_value = int(id_value)
            all_id[new_idtype] = id_value
        return all_id

    @property
    def protein(self):
        sql = "SELECT Sequence FROM seq_db WHERE KEY_ID = {}". format(
            self.id_dict['KEY_ID'])
        seq = self.database.query(sql, dict_cursor=True)[0]['Sequence']
        return ProteinSeq(seq)

    def cs_data(self, element=None):

        """
        :return: [(Correlation_1, cs_), Correlation_m, cs_m) ]
        """
        correltaitons = []

        for res in aminoacids.aa_list:
            sql = '''
            SELECT x.KEY_ID, x.ATOM_NAME,
            SUBSTRING_INDEX(GROUP_CONCAT(x.SND_STRC
            ORDER BY x.occurrences DESC SEPARATOR ':::'), ':::', 1)
            AS SND_STRC_MODE, x.C_SHIFT
            FROM(SELECT strc.KEY_ID, cs.ATOM_NAME, strc.SND_STRC,
            cs.C_SHIFT, COUNT(*) as occurrences
            FROM {0}_strc_db AS strc LEFT JOIN {0}_cs_db as cs
            ON strc.KEY_ID = cs.KEY_ID
            WHERE strc.FIRSTKEY_ID = {1}
            GROUP BY strc.KEY_ID, strc.SND_STRC, cs.ATOM_NAME) as x
            GROUP BY x.KEY_ID, x.ATOM_NAME'''. \
                format(res, self.id_dict['KEY_ID'])

            matches = self.database.query(sql, dict_cursor=True)

            if len(matches) == 0:
                continue

            for match in matches:

                atom = match['ATOM_NAME']
                if element:
                    try:
                        if atom[0] != element:
                            continue
                    except TypeError:
                        pass

                ss = match['SND_STRC_MODE']
                cs = match['C_SHIFT']

                if atom is None:
                    continue

                # Set the correct secondary-structure.
                if ss in ['I', 'G']:
                    ss = 'H'
                elif ss in ['B', 'b']:
                    ss = 'E'
                elif ss == 'T':
                    ss = 'C'
                if atom not in ['C', 'CA', 'CB', 'H', 'N']:
                    ss = 'X'

                key = Correlation(res, (atom, ), ss)
                correltaitons.append((key, cs))

        return correltaitons
