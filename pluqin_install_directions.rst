Step 0: Install Python 2.7
--------------------------
If you have python installed go to Step 1. It is a bad idea to use your default
system python. On a Mac you can install python 2.7 from homebrew using the
these directions. If not on a Mac we suggest you look at:
http://docs.python-guide.org/en/latest/

::
    bash
    /usr/bin/ruby -e "$(curl -fsSL
    https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install python

Step 1.a: Install a virtualenv
------------------------------
If you have virtualenv installed move to Step 1.b. It is highly suggested that
you work in a virtual environment.

::
    pip2.7 install virtualenv

Step 1.b: Activate virtualenv
-----------------------------
cd <to/directory/where/pluq/is>

::
    mkdir pluq_env
    mv pluq pluq_env/pluq
    cd pluq_env
    virtualenv env
    bash
    source env/bin/activate

Step 2: Install Python dependencies and pluq
--------------------------------------------
::
    cd pluq
    pip install -r requirements.txt
    python setup.py install


