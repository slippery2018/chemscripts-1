from numpy import loadtxt, nan
from re import findall


def excitations(file):
    excitations = loadtxt(findall('(?<=Excitation energy \/ cm\^\(-1\)\:).*', open(file).read()))
    return excitations


def twoCcheck(file):
    istwoC = False
    with open(file, 'r') as f:
        for line in f.readlines():
            if 'Two-component modus switched on ! ' in line:
                istwoC = True
    return istwoC


def _oneCoscvelrep(file):
    velrep = loadtxt(findall('(?<=velocity representation\:).*', open(file).read()))[0::2]
    return velrep


def _oneCosclenrep(file):
    lenrep = loadtxt(findall('(?<=length representation\:).*', open(file).read()))[0::2]
    return lenrep


def _oneCoscmixrep(file):
    mixedrep = loadtxt(findall('(?<=mixed representation\:).*', open(file).read()))[0::1]
    return mixedrep


def _twoCoscvelrep(file):
    velrep = loadtxt(findall('(?<=velocity representation\:).*', open(file).read()))[0::3]
    return velrep


def _twoCosclenrep(file):
    lenrep = loadtxt(findall('(?<=length representation\:).*', open(file).read()))[0::3]
    return lenrep


def _twoCoscmixrep(file):
    mixedrep = loadtxt(findall('(?<=mixed representation\:).*', open(file).read()))[0::2]
    return mixedrep


def _twoCtaulenrep(file):
    lenrep = loadtxt(findall('(?<=length representation\:).*', open(file).read()))[1::3]
    return lenrep


def _twoCtaumixrep(file):
    mixedrep = loadtxt(findall('(?<=mixed representation\:).*', open(file).read()))[1::2]
    return mixedrep


def _twoCtauvelrep(file):
    velrep = loadtxt(findall('(?<=velocity representation\:).*', open(file).read()))[1::3]
    return velrep


def oscvelrep(file):
    if twoCcheck(file):
        velrep = _twoCoscvelrep(file)
    else:
        velrep = _oneCoscvelrep(file)
    return velrep


def osclenrep(file):
    if twoCcheck(file):
        lenrep = _twoCosclenrep(file)
    else:
        lenrep = _oneCosclenrep(file)
    return lenrep


def oscmixrep(file):
    if twoCcheck(file):
        mixrep = _twoCoscmixrep(file)
    else:
        mixrep = _oneCoscmixrep(file)
    return mixrep


def tauvelrep(file):
    if twoCcheck(file):
        velrep = _twoCtauvelrep(file)
    else:
        velrep = nan
    return velrep


def taulenrep(file):
    if twoCcheck(file):
        lenrep = _twoCtaulenrep(file)
    else:
        lenrep = nan
    return lenrep


def taumixrep(file):
    if twoCcheck(file):
        mixrep = _twoCtaumixrep(file)
    else:
        mixrep = nan
    return mixrep
