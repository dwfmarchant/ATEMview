
import pandas as pd
import numpy as np

def readObsPred(obsName, predName):

    with open(obsName, 'r') as f:
        obsLines = pd.Series(f.readlines())
    obsLines = obsLines.str.strip()
    obsLines = obsLines.str.split()
    obsLines = obsLines[obsLines.apply(len) == 22]

    dat = pd.DataFrame()
    dat['x'] = obsLines.apply(lambda x: float(x[0]))
    dat['y'] = obsLines.apply(lambda x: float(x[1]))
    dat['z'] = obsLines.apply(lambda x: float(x[2]))
    dat['t'] = obsLines.apply(lambda x: float(x[3]))
    dat['dBdt_Z'] = obsLines.apply(lambda x: float(x[20]))
    dat['dBdt_Z_UN'] = obsLines.apply(lambda x: float(x[21]))
    dat['dBdt_Z_pred'] = np.loadtxt(predName, usecols=[-1])
    dat = dat.reset_index(drop=True)

    # Set locInd, tInd
    a = dat[['x', 'y']].values
    b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, ic = np.unique(b, return_inverse=True)
    icS = pd.DataFrame(ic, columns=['uInd']).drop_duplicates().reset_index(drop=True)
    icS['locInd'] = icS.index.copy()
    dat['locInd'] = icS.set_index('uInd').loc[ic, 'locInd'].values

    _, dat['tInd'] = np.unique(dat.t, return_inverse=True)

    return dat
