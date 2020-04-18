# In the style of http://systrom.com/covid19-charts-us-states/

import re
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def powerscale(p):
    return (lambda x: x**(1./p), lambda x: x**p)


def format_log10(x, pos):
    return re.sub('0000$', '0K', f'{x:.0f}')


_, dataroot, out = sys.argv

# Gray is the new black.
for k in ('text.color', 'axes.edgecolor', 'axes.labelcolor', 'xtick.color', 'ytick.color'):
    plt.rcParams[k] = '.4'

fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
ax.set_title('COVID-19 Cases by States as of TODO')
ax.set_xlabel('Days since 100 cases')
ax.set_yscale('function', functions=powerscale(5))
ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(7))
ax.yaxis.set_major_locator(mpl.ticker.LogLocator())
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_log10))
ax.grid(c='.9')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for state in sys.stdin:
    state = state.strip()
    d = np.loadtxt(f'{dataroot}/{state}.csv', delimiter=',')
    p = ax.plot(d[:,0], d[:,1], marker='.', mfc='w')
    color = p[-1].get_color()
    ax.annotate(state, d[-1],
                bbox=dict(boxstyle='round4', fc='w', color=color),
                color=color)

# Plot doubling guide lines without extending view limits.
xmax = ax.get_xlim()[1]
ymax = ax.get_ylim()[1]
x = np.arange(0, 50, .1)
for d in [1, 2, 3, 7]:
    y = 100 * 2**(x/d)
    ax.plot(x, y, ':', c='.7', zorder=1)
    # Find the position of the guide at the view limit.
    i = min(np.searchsorted(x, xmax-2), np.searchsorted(y, ymax-5e4))
    ax.annotate(f'{d}d', (x[i], y[i]),
                xytext=(-25, 0), textcoords='offset points', c='.7')
ax.set_xlim(0, xmax)
ax.set_ylim(100, ymax)

fig.savefig(out)
