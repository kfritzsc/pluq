#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
======
PLUQin
======

A program to help assign protein chemical shift peaks. Especially
helpful for assigning chemical shift correlations in a 2D plane. The
data used by this program comes from the PIQC [1] analysis of the
PACSY/BMRB [2] database.

All possible intra-residue chemical shift assignments within a given
confidence level are provided. The possible assignments are ranked by
likelihood using probability density functions determined with
non-parametric methods. If desired you can truncate the assignment at
a certain likelihood. If you are worried about miss-grouping peaks,
keep the cut-off value negative, this returns all possibilities for
each resonance even if some options are missing peaks and can not be
assigned. The program also provides secondary structure (H:C:E
probability). The probabilities will be adjusted based on the
sequence if it is provided, by default the probabilities are adjusted
to the average amino-acid frequencies.

Experiments
------------

- 2D Carbon 1-bond: cc
- 2D Carbon-Nitrogen 1-bond (ie. mostly CA-N ): cn
- 1D Carbon: c
- 1D Nitrogen: n
- 1D Proton: h

If you know a little python it is pretty easy to add new experiments
but you will need the full version of the PACSY database with the
PIQC tables. See'utility/build_exp_pdf.py' for an example.

Warning
--------
No Database Chemical Shifts for: Trp-(CD2)-All, Trp-(CG)-All
Glu-(HE2)-All, Asp-(HD2)-All, Lys-(HZ1)-All, Pro-(H2)-All,
Pro-(H3)-All, Tyr-(HH)-All, Asp-(CB,CG)-Sheet, Asp-(CG,CB)-Sheet,
His-(CG,CB)-Coil, Trp-(CZ2,CE2)-All, Trp-(CD2,CE3)-All,
Trp-(CB,CG)-Helix, Trp-(CB,CG)-Coil, Trp-(CG,CB)-Helix,
Trp-(CG,CB)-Coil, Trp-(CE3,CD2)-All, Trp-(CE2,CZ2)-All,
Tyr-(CB,CG)-Coil Tyr-(CG,CB)-Coil, Lys-(CE,NZ)-All, Pro-(CA,N)-Coil,
Pro-(CD,N)-Helix, Pro-(CD,N)-Sheet, Thr-(CA,N)-Helix

References
----------

1. K. J. Fritzsching, Mei Hong,  K. Schmidt-Rohr. "Conformationally
    Selective Multidimensional Chemical Shift Ranges in Proteins from
    a PACSY Database Purged Using Intrinsic Quality Criteria " J.
    Biomol. NMR 2016b doi:10.1007/s10858-016-0013-5

2. Lee, W.; Yu, W.; Kim, S.; Chang, I.; Lee, W. PACSY, a Relational
    Database Management System for Protein Structure and Chemical
    Shift Analysis. J Biomol NMR 2012, 54 (2),169–179.
    doi: 10.1007/s10858-012-9660-3

Please cite the two references if use of this code leads to
publication.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__version__ = '0.2.1.0'

if __name__ == "__main__":
    import argparse
    from pluq.pluqin import main

    # Set up command line options.
    parser = argparse.ArgumentParser(
        description="""PLUQin: returns a table of possible
        intra-residue assignments and there likelihoods based on
        input chemical shifts and optionally the sequence. They are
        sorted first by the assignment joint probability and then by
        the sum of the individual probabilities.""",

        epilog=""" Fritzsching, Hong, Schmidt-Rohr. J. Biomol. NMR
        2016 doi:10.1007/s10858-016-0013-5""")

    parser.add_argument(
        "-p", "--peak",
        action='append',
        type=float,
        nargs='+',
        help="""Chemical shifts, examples: -p 55 -p 18 (if exp_name
        is 1D) -p 55 18 (if exp_name is 2D.""")

    parser.add_argument(
        "-e", "--exp_name",
        default='c',
        choices=['c', 'h', 'n', 'cc', 'cn'],
        help="Experiments available: c, n, h, cc, cn")

    parser.add_argument(
        "-c", "--cut_off",
        action="store",
        type=float,
        default=-1,
        help="""Cut off %% value, input a negative number for
        everything.""")

    parser.add_argument(
        "-s", "--seq",
        action="store",
        type=str,
        default='',
        help="Protein sequence in 1-letter amino-acid code.")

    # Parse the options.
    parser_dict = vars(parser.parse_args())

    if parser_dict['peak'] is None:
        parser.error('Use pluqin.py -h to see options.')

    cs_set = parser_dict['peak']
    exp_name = parser_dict['exp_name']
    cut_off = parser_dict['cut_off']
    seq = parser_dict['seq']

    table = main(cs_set, exp_name, seq=seq)

    # Pretty Printing
    print('input: {}'.format(', '.join(map(str, cs_set))))
    print('experiment: {}'.format(exp_name))

    if table is None:
        print('No chemical shifts were found!')

    else:
        n = len(cs_set)
        header = ['AA'] + ['p{}'.format(x+1) for x in range(n)]*2
        header += ['Joint', 'H', 'C', 'E']
        cols = [list(x) for x in zip(*table)]
        col_widths = [max(map(len, map(str, x))) for x in cols]
        fmt = '  '.join(['{{:<{}}}'.format(width) for width in
                         col_widths])

        print(fmt.format(*header))
        for line in table:

            if line[-4] <= cut_off:
                break
            line = map(str, [x if x else '-' for x in line])
            print(fmt.format(*line))
