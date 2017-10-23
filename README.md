
# pluq


Python tools for analyzing the PACSY NMR chemical shift database and assigning
protein chemical shifts. 


## Requirements

- Python 2.7+ or Python 3.4+
- GEOS
- GDAL

### To install the requirements on a Mac you could use Homebrew

```bash
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    
    brew install python3
    brew install geos
    brew install gdal
```

## Install


```bash
    cd <path/to/pluq>/pluq
    pip3 install -r requirements.txt
    python3 setup.py install
```

## References

1. K. J. Fritzsching, Mei Hong,  K. Schmidt-Rohr. "Conformationally
    Selective Multidimensional Chemical Shift Ranges in Proteins from
    a PACSY Database Purged Using Intrinsic Quality Criteria " J.
    Biomol. NMR 2016 doi:10.1007/s10858-016-0013-5
2. Lee, W.; Yu, W.; Kim, S.; Chang, I.; Lee, W. PACSY, a Relational
    Database Management System for Protein Structure and Chemical
    Shift Analysis. J Biomol NMR 2012, 54 (2),169–179.