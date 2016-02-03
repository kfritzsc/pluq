#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Connect to an empty PACSY database and fill it from the CSV tables provided
on the PACSY website.

KJF, Updated 2016-01-20
"""

import os
import csv
import time
import MySQLdb


def load_pacsy(csv_dir_file_path, database, exclude_strings=None):
    """Connect to an empty PACSY database and fill it from the CSV tables
    provided on the PACSY website.

    :param csv_dir_file_path: full path to directory with CSV files
    :param database: database initiated with table descriptions
    :param exclude_strings: list of string that partially match unwanted files
    """
    cursor = database.cursor()

    file_list = os.listdir(csv_dir_file_path)
    file_list = [f for f in file_list if
                 all([x not in f for x in exclude_strings])]

    for n, file_name in enumerate(file_list):
            # Get the table name.
            table_name = os.path.splitext(file_name)[0].upper()

            # A very simple hidden file check, if other hidden files exist
            # change this condition appropriately, I do not have a good way to
            # catch all possible hidden files...
            if table_name[0] == '.':
                continue

            # Put all the data into a table.
            fid = open(os.path.join(csv_dir_file_path, file_name))
            data = csv.reader(fid)

            print 'Working on {} table.'.format(table_name)

            # Inset all the data one row at a time.
            for data_line in data:
                data_line = tuple(data_line)
                sql = 'INSERT INTO {} VALUES {}'.format(table_name, data_line)
                try:
                    cursor.execute(sql)
                # Probably something wrong with the loaded schema.
                except Exception as e:
                    print Exception,  e

            # Commit to the database after every file.
            database.commit()
            fid.close()


if __name__ == '__main__':
    # Ran in 28 min on KJF's Mac Pro.

    # Open database connection.
    db = MySQLdb.connect("localhost", "root", "pass", "pacsy2")
    # file_path = '/Users/kjf/Downloads/zavot/data/whlee/pacsy/CSV_122815'
    file_path = '/Users/kjf/git/pluqin_env/pluq/scripts/build_pacsy/build_pacsy/piqc_db'

    t0 = time.time()

    # Exclude files from directory if they have any of these stings in them.
    exclude = ['COORD', 'PDBSEQ', 'DC_', 'AC_']

    load_pacsy(file_path, db, exclude_strings=exclude)

    t = (time.time()-t0) / 60
    print('This took {} min.'.format(t))
