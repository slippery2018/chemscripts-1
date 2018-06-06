#!/usr/bin/python3

'''
This script uses parseGAUSSIAN to extract gradient vectors from an output file and prints data to the screen
'''


def GRADbilder(GRAD):
    '''
    This function returns the formatted .bild for the input NAC

    reads in a vector from parseGAUSSIAN

    returns tuple containing strings with terminated with newlines

    '''

    # Norm the GRAD
    GRADmag = np.linalg.norm(GRAD, 'fro')
    nGRAD = np.divide(GRAD, GRADmag)

    GRADbild = ()

    # Vector settings
    arrow_color = "cornflower blue"
    # Scales magnitude of vector
    scale_fact = args["mult"]
    # radius of the stick. This should be >1
    arrow_stk_rad = ".1"
    # radius of the base of the tip cone. This should be ~4*arrow_stk_rad
    arrow_tip_rad = ".2"
    # fraction of total vector length taken up by stick
    arrow_stk_frc = "0.75"

    # Get the atom coordinates
    coords = infile.atomcoords[0]

    # Create the t
    GRADbild = GRADbild + (".color {}".format(arrow_color), )
    # For each atom, add a line to the tuple
    for atom in range(infile.natom):
        # Omit very short vectors
        if np.linalg.norm(nGRAD[atom]) > args["cut"]:
            vec_start = coords[atom]
            vec_end = vec_start + np.multiply(nGRAD[atom], scale_fact)
            # GRADbild = GRADbild + (".arrow {} {} {} {} {} {}".format(vec_start[0], vec_start[1], vec_start[2], vec_end[0], vec_end[1], vec_end[2]), )
            GRADbild = GRADbild + (".arrow {:2.6f} {:2.6f} {:2.6f} {:2.6f} {:2.6f} {:2.6f} {} {} {}".format(vec_start[0], vec_start[1], vec_start[2], vec_end[0], vec_end[1], vec_end[2], arrow_stk_rad, arrow_tip_rad, arrow_stk_frc), )

    return GRADbild


import argparse
import numpy as np
import parseGAUSSIAN as pG
import cclib
import os.path


parser = argparse.ArgumentParser(description="This script extracts non-adiabatic couplings from a G09 file and prints them to the screen in the Chimera .bild format")
parser.add_argument("-i", dest="file", metavar="file", help="input G09 calculation", required=True)
parser.add_argument("-q", dest="quiet", help="don't print to screen", required=False, default=False, action='store_true')
parser.add_argument("-s", dest="save", help="save to file, with name <input file>.gradient.bild", default=False, action='store_true')
parser.add_argument("-c", dest="cut", metavar="cut", help="threshold for atomic contributions, as a fraction. Default = 0.02. (very short vectors look bad)", default=0.02, required=False)
parser.add_argument("-m", dest="mult", metavar="mult", help="multiplicative factor for increasing the size of the vector. Default = 2.", default=2, required=False)
args = vars(parser.parse_args())

infile = cclib.parser.ccopen(args["file"]).parse()

gradvec = pG.gradient(args["file"])

bild = GRADbilder(gradvec)
if not args["quiet"]:
    for line in range(len(bild)):
        print('{}'.format(bild[line]))
if args["save"]:
    basename = os.path.basename(args["file"])[:-4]
    thisname = '{}.gradient.bild'.format(basename)
    if not os.path.exists(thisname):
        with open(thisname, 'a') as bild_file:
            for line in range(len(bild)):
                bild_file.write('{}\n'.format(bild[line]))
    else:
        print('Warning, {} already exists!'.format(thisname))
