#pluq

Python tools for analyzing the PACSY NMR chemical shift database and assigning
chemical shifts


## Install
### Step 1.a: Install Python 2.7+ or Python 3.4+###

If you have python installed go to Step 1. It is a bad idea to use
your default system python. On a Mac you can install python from
homebrew using the these directions. If not on a Mac we suggest you
look at: http://docs.python-guide.org/en/latest/

```bash
    /usr/bin/ruby -e "$(curl -fsSL
    https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install python3
```

### Step 1.b: Install two c-libraries  GEOS and GDAL required by Shapely and Fiona ###

```bash
    brew install geos
    brew install gdal
```


### Step 2: Install Python dependencies and pluq ###

```bash
    git clone https://github.com/kfritzsc/pluq.git
    cd pluq
    pip3 install -r requirements.txt
    python3 setup.py install
```


## References ##

1. K. J. Fritzsching, Mei Hong,  K. Schmidt-Rohr. "Conformationally
    Selective Multidimensional Chemical Shift Ranges in Proteins from
    a PACSY Database Purged Using Intrinsic Quality Criteria " J.
    Biomol. NMR 2016 doi:10.1007/s10858-016-0013-5

2. Lee, W.; Yu, W.; Kim, S.; Chang, I.; Lee, W. PACSY, a Relational
    Database Management System for Protein Structure and Chemical
    Shift Analysis. J Biomol NMR 2012, 54 (2),169–179.