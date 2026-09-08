import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tests.original.plotFeasibleRegion_helper import plotFeasibleRegion

def test_plotFeasibleRegion_plot():
    plt.close('all')
    x = [0, 1, 1, 0, 0]
    y = [0, 0, 2, 2, 0]
    plotFeasibleRegion(x, y)
    figs = list(map(lambda f: f, plt.get_fignums()))
    assert len(figs) > 0