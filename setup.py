from io import open
from os import path
from setuptools import setup

# Get the long description from the readme
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pluq',
      version='0.2.0',
      description='Tools for working with the PACSY database.',
      long_description=long_description,
      keywords='Protein NMR-Chemical-Shift PACSY re-referencing',
      url='http://github.com/kfritzsc/pluq',
      author='Keith Fritzsching',
      author_email='kfritzsc@brandeis.edu',
      license='MIT',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7'],
      packages=['pluq'],
      package_dir={'pluq': 'pluq'},
      package_data={'pluq': ['data/pdf/*', 'data/piqc_db/*',
                             'data/regions/cc_region_all/*']},
      scripts=['scripts/pluqin.py'],
      install_requires=['numpy', 'scipy', 'matplotlib', 'fiona', 'shapely',
                        'sklearn', 'h5py'],
      include_package_data=True,
      zip_safe=False)
