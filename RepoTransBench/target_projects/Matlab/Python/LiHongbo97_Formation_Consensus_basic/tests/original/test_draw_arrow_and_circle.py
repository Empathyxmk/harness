import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lihongbo_consensus.helpers import draw_arrow, draw_circle

def test_draw_arrow_and_circle():
    X = [0, 1]
    Y = [0, 1]
    f1 = plt.figure()
    draw_arrow(0, 0, 1, 1, 'r')
    plt.close(f1)

    f2 = plt.figure()
    draw_circle([0, 0], 1)
    plt.close(f2)