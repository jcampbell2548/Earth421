import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def colorbar(mappable):
    ax = plt.gca()
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.5)
    return fig.colorbar(mappable, cax=cax)
