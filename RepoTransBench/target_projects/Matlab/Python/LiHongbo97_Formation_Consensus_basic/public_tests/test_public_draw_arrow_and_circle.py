import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lihongbo_consensus.helpers import draw_arrow, draw_circle

def test_public_draw_arrow_and_circle():
    h = plt.figure()
    try:
        draw_arrow([2, 2], [6, 7])
        draw_circle([4, 3], 1.5)
        plt.close(h)
    except Exception:
        plt.close(h)
        assert False