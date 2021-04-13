from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from math import pi, cos, sin
import os

import numpy as np
from pyproj import Transformer

from matplotlib import patches
import matplotlib
matplotlib.use('Agg')

plt.rcParams.update({'font.size': 6})
plt.rcParams["font.family"] = "Times New Roman"

song = FontProperties(
    fname='/usr/share/fonts/truetype/windows-font/simsun.ttc', size=6)
fontcn = {'fontproperties': song, 'size': 6, 'weight': 'normal'}
legendfont = FontProperties(
    fname='/usr/share/fonts/truetype/windows-font/simsun.ttc', size=6)

def plot(idx:"str"):
    plt.figure(figsize=(3, 3))
    abs_data = np.loadtxt(os.path.join("/mnt/sdb/xuefeng/kitti_odom/sequences/cropped",idx, "result.txt"))
    # abs_data = np.genfromtxt("/home/xuefeng/data/tiev_odom/04/result/result.csv", delimiter=",", skip_header=1)
    abs_x = abs_data[:, 1]
    abs_y = abs_data[:, 3]
    plt.plot(abs_x, abs_y, color='b', linewidth=1)
    plt.grid()
    plt.axis("equal")
    plt.xlabel("X(m)")
    plt.ylabel("Y(m)")
    plt.savefig(f"result_{int(idx)}.png", bbox_inches='tight', dpi=300)


plot("01")
