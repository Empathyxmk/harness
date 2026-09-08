import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tests.original.plotFeasibleRegion_helper import plotFeasibleRegion

def test_public_plotFeasibleRegion():
    xlim_pub = [0, 1]
    ylim_pub = [0, 2]
    region_pub = [(0.2, 0.4), (0.5, 1.5)]
    try:
        plotFeasibleRegion(xlim_pub, ylim_pub, region_pub)
    except Exception as e:
        assert False, f"plotFeasibleRegion crashed! {str(e)}"