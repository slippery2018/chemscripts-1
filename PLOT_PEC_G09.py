#!/usr/bin/python3

import numpy as np
import re
import cclib
import os
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt


def getstaten(n, excitations):
    excit = []
    for key in excitations.keys():
        excit.append(excitations[key][n])
    return excit


# globals
angstrtobohr = 1.88973
cmtoeV = 1 / 8000

# Create a list of the files ending with .out in the working directory
list = glob.glob("{}/*.log".format(os.getcwd()))

# Create an array containing ccread objects of the files found
files = []
for i in range(0, len(list)):
    files.append(cclib.io.ccread(list[i]))

# # Prepare the dictionary which will contain ccread objects with keys of Q
# pointsdict = {}
# # Figure out Q from the name of the file, then put the  with Q as the key
# for i in range(len(list)):
#     q = int(re.findall('.{2}(?=[l,r,q])', list[i])[0])
#     # If Q is on the left, it is negative
#     if re.search('[0-9][0-9][l]', list[i]) is not None:
#         q = -q
#     pointsdict[q] = files[i]

# # Prepare a dictionary of SCF energies
# scfenergies = {}
# for key in pointsdict:
#     scfenergies[key] = pointsdict[key].scfenergies[0]

# Prepare a dictionary of SCF energies
FilesNoOrder = {}
for i in range(0, len(list)):
    FilesNoOrder[i] = files[i]

scfenergiesNoOrder = {}
for key in FilesNoOrder:
    scfenergiesNoOrder[key] = FilesNoOrder[key].scfenergies[0]

# Find the index of lowest energy point
index_min = min(scfenergiesNoOrder, key=scfenergiesNoOrder.get)

# Prepare a dictionary containing distance from minimum point
pointsdist = {}
for i in range(0, len(list)):
    dist = np.sum((files[i].atomcoords - files[index_min].atomcoords))
    pointsdist[i] = dist * angstrtobohr

# Prepare points dict with keys that are the pointsdists
pointsdict = {}
for i in range(0, len(list)):
    pointsdict[pointsdist[i]] = files[i]

# Real SCF dict
scfenergies = {}
for i in range(0, len(list)):
    scfenergies[pointsdist[i]] = files[i].scfenergies[0]

# Prepare a dictionary containing relative SCF energies
relscfs = {}
for key in pointsdict:
    relscfs[key] = scfenergies[key] - scfenergiesNoOrder[index_min]

# Prepare a dictionary containing relative excited state energies
relexcit = {}
for key in pointsdict:
    try:
        relexcit[key] = pointsdict[key].etenergies * cmtoeV + relscfs[key]
    except AttributeError:
        continue

# Set up mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [
    r'\usepackage{txfonts}',
    r'\usepackage{sansmath}',
    r'\renewcommand*\sfdefault{phv}',
    r'\renewcommand{\familydefault}{\sfdefault}',
    r'\sansmath']
# Set up the plot
fig = plt.figure()
ax1 = fig.add_subplot(111)
# plot GS energies
gs_x, gs_energies = zip(*sorted(zip(relscfs.keys(), relscfs.values())))
ax1.plot(gs_x, gs_energies, '-', lw=1, c='gray')
for i in range(len(relexcit[0])):
    # clr = "C" + str(i)
    x, es_energies = zip(*sorted(zip(relexcit.keys(), getstaten(i, relexcit))))
    ax1.plot(x, es_energies, '-', lw=1)
plt.xlabel('Distance from $Q = 0$ / bohr')
ax1.set_ylabel('Energy / eV')
# # ax2 is for showing the distance
# ax2 = ax1.twiny()
# gs_x, gs_dist = zip(*sorted(zip(pointsdist.keys(), pointsdist.values())))
# ax2.plot(gs_dist, gs_energies, '-', lw=1, c='gray')
# ax2.set_xlabel('Distance from $Q = 0$ / bohr')
# Change formatting and plot
fig.tight_layout()
plt.show()
