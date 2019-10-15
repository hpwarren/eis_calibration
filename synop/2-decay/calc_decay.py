import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from decay_tanh import decay_tanh
from decay_exp import decay_exp
import sys

def read_df(file, element, ion):
    df = pd.read_pickle(ipf)
    print(ipf)
    match, = np.where((df['element'] == element) & (df['ion'] == ion))
    df = df.iloc[match]
    print(df)
    ints = np.array(df['intensity'])
    ts = np.array(df['mission_sec'])/(86400*365.25)
    this_df = df.iloc[0]
    line_id = this_df['element'] + ' ' + this_df['ion'] + ' ' + f'{this_df["wave"]:.3f}'
    return ts, ints, line_id


options = ['He II', 'Si VII', 'Fe VIII', 'Fe X']
for n, opt in enumerate(options):
    print(f' {n+1} {opt}')
n = input(' Select an option > ')
try:
    element, ion = (options[int(n)-1]).split(' ')
except:
    exit()

ipf = '../1-ints/ints_synop.pickle'
ts_synop, ints_synop, line_id = read_df(ipf, element, ion)
ipf = '../1-ints/ints_full_ccd.pickle'
ts_full_ccd, ints_full_ccd, line_id = read_df(ipf, element, ion)

popt, pcov = curve_fit(decay_tanh, ts_synop, ints_synop, p0=[200,-0.5,0.5])
print(popt)
yfit_tanh = decay_tanh(ts_synop, *popt)

popt, pcov = curve_fit(decay_exp, ts_synop, ints_synop, p0=[200,0.5])
print(popt)
yfit_exp = decay_exp(ts_synop, *popt)

residual_tanh = 100*(ints_synop - yfit_tanh)/ints_synop
residual_exp = 100*(ints_synop - yfit_exp)/ints_synop

title = line_id

ms = 10
fig, ax = plt.subplots(2, 1, figsize=(9,7))

ax[0].scatter(ts_synop, ints_synop, color='black', s=ms, label='SYNOP')
ax[0].scatter(ts_full_ccd, ints_full_ccd, color='red', s=ms, label='FULL CCD')
ax[0].plot(ts_synop, yfit_tanh, color='orange', label='tanh')
ax[0].plot(ts_synop, yfit_exp, color='blue', label='exp')
ax[0].set_ylabel('Intensity')
ax[0].set_title(title)

ax[1].scatter(ts_synop, residual_tanh, color='orange', s=ms)
ax[1].scatter(ts_synop, residual_exp, color='blue', s=ms)
ax[1].set_ylim((-50,50))
ax[1].axhline(0)
ax[1].set_xlabel('Years Since Launch')
ax[1].set_ylabel('Residual (%)')

ax[0].legend()

opf = 'calc_decay_' + element + '_' + ion + '.png'
plt.savefig(opf)
print(' + saved to ' + opf)
plt.show()

