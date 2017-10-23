# -*- coding: utf-8 -*-
"""
Script to plot 2D chemical shift ranges, optionally from a custom shape_file.
"""
import matplotlib
matplotlib.rcParams['svg.fonttype'] = 'none'


import os
import fiona
from shapely.geometry import shape
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# Define the shape file structure.
# MultiPolygon with one attribute
schema = {'geometry': 'Polygon',
          'properties': {'corr': 'str',
                         'levels': 'float',
                         'bandwidth': 'float'}}

greek_dict ={
    u'A': u'α',
    u'B': u'β',
    u'G': u'γ',
    u'D': u'δ',
    u'E': u'ε',
    u'H': u'η',
    u'Z': u'ζ',}

facecolors = {'Helix': 'Red',
              'Coil': 'Blue',
              'Sheet': 'Green',
              'All': 'none',
              None: 'none'}

edgecolors = {'Helix': 'Red',
              'Coil': 'Blue',
              'Sheet': 'Green',
              'All': 'Black',
               None: 'Black'}
import pluq.aminoacids

aa_1let = {x[1]: x[0] for x in pluq.aminoacids.aa_3let.items()}


if __name__ == "__main__":
    # shape file path
    dir_name = os.path.dirname(os.path.dirname(__file__))

    # /Users/kjf/git/pluqin_env/pluq/pluq/data/regions_2d/roi_2dcc.shp
    shape_file = '/Users/kjf/git/pluq/pluq/data/regions/cc_region_all/cc_region_all.shp'



    # for aa in pluq.aminoacids.aa_list:
    aa = 'V'
    with fiona.open(shape_file, 'r', 'ESRI Shapefile', schema) as shp:

        fig = plt.figure(1, figsize=(7, 4.5))
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 2.95445],)

        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1], sharey=ax1)
        plt.setp(ax2.get_yticklabels(), visible=False)

        labels= []
        positions =[]

        for s in shp:

            res, atoms, ss = s['properties']['corr'].split('-')
            res = aa_1let[res]

            level = s['properties']['levels']

            if res != aa:
                continue

            if level not in [69, 80]:
                continue

            region = shape(s['geometry'])



            if level== 80 and ss in ['Coil', 'X', 'None']:
                center = region.centroid
                positions.append((center.x, center.y))
                atoms = atoms[1:-1]
                atoms = [x.strip() for x in atoms.split(',')]

                if ss in ['All', None] and atom[0] in ['C', 'CA', 'CB']:
                    continue

                if ss in ['All', None] and atom[1] in ['C', 'CA', 'CB']:
                    continue

                unicode_atoms = []
                # print atoms
                for atom in atoms:
                    if len(atom)==1:
                        unicode_atoms.append(atom)
                    else:
                        name = u'{}'.format(atom[0])
                        name += u'{}'.format(greek_dict[atom[1]])
                        name += u'{}'.format(atom[2:])
                        unicode_atoms.append(name)

                labels.append(', '.join(unicode_atoms))


            patch1 = PolygonPatch(region,
                                 facecolor=facecolors[ss],
                                 edgecolor=edgecolors[ss],
                                 alpha=0.3)

            patch2 = PolygonPatch(region,
                     facecolor=facecolors[ss],
                     edgecolor=edgecolors[ss],
                     alpha=0.3)

            ax1.add_patch(patch1)
            ax2.add_patch(patch2)



    ax2.plot([10, 75], [10, 75], 'k--')
    for ax in [ax1, ax2]:
        for position, label in zip(positions, labels):
            ax.text(position[0], position[1],
                    str('('+label+')'),
                    verticalalignment='bottom', horizontalalignment='center')


    ax1.set_xlim([167, 189])
    ax1.set_ylim([10, 75])
    ax1.xaxis.set_ticks([170, 180 ])
    ax1.invert_yaxis()
    ax1.invert_xaxis()
    ax1.set_ylabel(u'Carbon-13 Chemical Shift (ppm from DSS)')

    ax2.set_xlim([10, 75])
    ax2.set_ylim([10, 75])
    ax2.invert_yaxis()
    ax2.invert_xaxis()
    ax2.set_xlabel(u'Carbon-13 Chemical Shift (ppm from DSS)')


    plt.suptitle(u'{}( C-C 2-bonds): 68%/85%'.format(pluq.aminoacids.aa_3let[aa]))

    plt.show()
     #plt.savefig(u'{}cc2b6885.svg'.format(pluq.aminoacids.aa_3let[aa]))
