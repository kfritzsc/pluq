
# pluq


Python tools for analyzing the PACSY NMR chemical shift database and assigning protein chemical shifts.


## Requirements

- Python 2.7+ or Python 3.4+
- GEOS
- GDAL

To install the requirements on a Mac you could use [Homebrew](https://brew.sh):

```bash
    brew install python3
    brew install geos
    brew install gdal
```

You can also satisfy the requirements using the python packages from  [Anaconda](https://anaconda.org/anaconda/python).


## Optional Requirements

To use the chemical shift assignment program  `pluqin` discussed in Ref. [1] you do not need to install the whole PACSY database.  

If however you would like to run `piqc` or use `pluq` to make PACSY database queries, etc. you will need to have have `MySQL` installed (or another SQL database server system). You will also need to download the data from the [PACSY website](http://pacsy.nmrfam.wisc.edu). See `pluq/scripts/build_pacsy` for more information.


## Install

```bash
    cd <path/to/pluq>/pluq
    pip3 install -r requirements.txt
    python3 setup.py install
```

If you would like to use `pluq` to run PACSY database queries you will need to have `MySQL` installed. If you have installed python2, you will need the package `MySQLdb`. If you have python3 installed you will need to install `mysqlclient`.

## References

If you find this package useful in your work please cite these two papers. 

1. K. J. Fritzsching, Mei Hong,  K. Schmidt-Rohr. "Conformationally
    Selective Multidimensional Chemical Shift Ranges in Proteins from
    a PACSY Database Purged Using Intrinsic Quality Criteria " J.
    Biomol. NMR 2016, 64 (2), 115–130
    [doi:10.1007/s10858-016-0013-5](https://doi.org/10.1007/s10858-016-0013-5)
2. Lee, W.; Yu, W.; Kim, S.; Chang, I.; Lee, W. PACSY, a Relational
    Database Management System for Protein Structure and Chemical
    Shift Analysis. J Biomol NMR 2012, 54 (2),169–179.
    [doi:10.1109/BIBMW.2012.6470267](https://doi.org/10.1109/BIBMW.2012.6470267)