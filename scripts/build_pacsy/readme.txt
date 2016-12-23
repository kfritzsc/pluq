Keith's PACSY/PIQC Notes
========================

Starting from scratch.
----------------------
total computer run time ~ 2.0 hours
1a) Import pacsy-defs.sql and piqc-def.sql into a MySQL database.
   - Sequal Pro makes this easy.
2a) Run load_pacsy.py to fill all the regular pacsy tables with data from .csv files.
   - Will have to  input:
        -- File path to the directory of .csv files.
        -- MySQL database name and credentials
3a) Run piqc.py to generate chemical shift and protein statistics tables.
    - Wil have to input:
       -- MySQL database name and credentials
       -- Output file names.
4a) Run load_pacsy.py to upload tables.
    - Will have to input:
        -- file path to the directory of two .csv file generated in step 3.
        -- MySQL database name and credentials


Monthly Updating of the SEQ_CS table.
----------------------
total computer run time < 30 minutes
1b) Run piqc.py to generate chemical shift and protein statistics tables.
    - Wil have to input:
       -- MySQL database name and credentials
       -- File path to cs_stats.txt
       -- Optional List of new key_id
       -- Output file name

    - If you don't give list of new key_id you need to delete the seq_cs table in the
    PACSY database.
2b) Run load_pacsy.py to upload tables.*
    - Will have to input:
        -- File path to the directory of the one file made in step 1b
        -- MySQL database name and credentials
    * data from files with be appends to the end of the appropriate table.

