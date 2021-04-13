from math import pi,cos,sin
import os

import numpy as np
from pyproj import Transformer

from matplotlib import patches
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams.update({'font.size': 6})
plt.rcParams["font.family"] = "Times New Roman"

song = FontProperties(fname='/usr/share/fonts/truetype/windows-font/simsun.ttc', size=6)
fontcn = {'fontproperties': song, 'size': 6, 'weight': 'normal'}
legendfont = FontProperties(fname='/usr/share/fonts/truetype/windows-font/simsun.ttc', size=6)


def rotate_xy(x, y, heading, degree=True):
    if degree == True:
        heading = heading * pi / 180
    rotate_x = np.copy(x) * cos(heading) - np.copy(y) * sin(heading)
    rotate_y = np.copy(x) * sin(heading) + np.copy(y) * cos(heading)
    return rotate_x, rotate_y


def plot(num:"str，gnss数据上级目录名", result_dir:"str，Abs-DSO结果名"):
    fig = plt.figure(figsize=(3,3))
    ax = fig.add_subplot(111)

    # plot KITTI trajectory
    #kitti_data = np.loadtxt("/mnt/sdb/xuefeng/kitti_odom/poses/00.txt")
    #kitti_data = np.reshape(kitti_data, (kitti_data.shape[0], 3, 4))
    #kitti_x = kitti_data[:, 0, 3]
    #kitti_y = kitti_data[:, 2, 3]
    #ax.plot(kitti_x[:1000], kitti_y[:1000], color='k', label="轨迹真值", linewidth=1)


    #plot Realsense GNSS trajectory
    gnss_data = np.loadtxt(os.path.join("/mnt/sdb/xuefeng/rs_odom", num, "gnss.txt"))
    lat = gnss_data[:,2]
    lon = gnss_data[:,3]
    transformer = Transformer.from_crs("epsg:4326", "epsg:32651")
    utm_x, utm_y = transformer.transform(lat, lon)
    utm_x = utm_x - utm_x[0]
    utm_y = utm_y - utm_y[0]
    utm_x = utm_x[abs(utm_x) < 1000]
    utm_y = utm_y[abs(utm_y) < 1000]
    rotate_utm_x, rotate_utm_y = rotate_xy(utm_x, utm_y, -87.1)
    ax.plot(rotate_utm_x, rotate_utm_y, label="轨迹真值", linewidth=1)
    rect = patches.Rectangle((rotate_utm_x[0]-2,rotate_utm_y[0]-2), 4, 4, linewidth=1, edgecolor='r', facecolor='none', label="起点")
    ax.add_patch(rect)

    # plot Realsense IMU trajectory
    # imu_data = np.loadtxt("/home/xuefeng/abs-dso/build/imu_result.txt")
    # imu_x = imu_data[:,0]
    # imu_y = imu_data[:,2]
    # ax.plot(imu_x, imu_y, label="IMU", linewidth=1)

    # plot TiEV GNSS trajectory
    # gnss_data = np.loadtxt("/home/xuefeng/data/tiev_odom/04/gnss_sync_0.txt", usecols=[0,1,2,3])
    # lat = gnss_data[:,1]
    # lon = gnss_data[:,2]
    # transformer = Transformer.from_crs("epsg:4326", "epsg:32651")
    # utm_x, utm_y = transformer.transform(lat, lon)
    # utm_x = utm_x - utm_x[0]
    # utm_y = utm_y - utm_y[0]
    # utm_x = utm_x[abs(utm_x) < 1000]
    # utm_y = utm_y[abs(utm_y) < 1000]
    # rotate_utm_x, rotate_utm_y = rotate_xy(utm_x, utm_y, -24)
    # ax.plot(rotate_utm_x[:300], rotate_utm_y[:300], color='k', label="轨迹真值", linewidth=1)

    # plot Abs DSO trajectory
    abs_data = np.loadtxt(os.path.join("/home/zhongxu/Abs_DSO_result", result_dir+".txt"))
    # abs_data = np.genfromtxt("/home/xuefeng/data/tiev_odom/04/result/result.csv", delimiter=",", skip_header=1)
    abs_x = abs_data[:,1]
    abs_y = abs_data[:,3]
    ax.plot(abs_x, abs_y, color='b', label="改进后算法", linewidth=1)

    # plot Abs DSO coarse tracking trajectory
    # ct_data = np.genfromtxt("/home/xuefeng/Abs-DSO/build/logs/trackinglog.csv", delimiter=",", skip_header=1)
    # ct_x = ct_data[:,4]
    # ct_y = ct_data[:,6]
    # ax.plot(ct_x, ct_y, label="粗追踪", linewidth=1)
    # idx = 180
    # ax.plot(ct_x[idx], ct_y[idx], marker='o', markersize=1, color='r')
    # ax.plot(rotate_utm_x[idx], rotate_utm_y[idx], marker='o', markersize=1, color='g')
    # print(ct_data[idx,8], gnss_data[idx,7]-84.1)

    # plot Stereo DSO trajectory
    # stereo_data = np.loadtxt("/home/xuefeng/stereo_dso/build/result.txt")
    # stereo_x = stereo_data[:,3]
    # stereo_y = stereo_data[:,11]
    # ax.plot(stereo_x, stereo_y, color='r', label="双目DSO", linewidth=1)

    # plot DSO trajectory
    # dso_data = np.loadtxt("/home/xuefeng/dso/build/result.txt")
    # dso_x = dso_data[:,1]
    # dso_y = dso_data[:,3]
    # ax.plot(dso_x, dso_y, color='r', label="改进前算法", linewidth=1)

    # plot AirSim trajectory
    # airsim_data = np.loadtxt("/mnt/sdb/xuefeng_data/airsim_odom/20201204/poses.txt")
    # airsim_x = airsim_data[:,3]
    # airsim_y = airsim_data[:,11]
    # ax.plot(airsim_x[10:], airsim_y[10:], label="AirSim", linewidth=1)
    # # rect = patches.Rectangle((airsim_x[10]-2,airsim_y[10]-2), 4, 4, linewidth=1, edgecolor='r', facecolor='none', label="Start Point")
    # rect = patches.Rectangle((airsim_x[680]-2,airsim_y[680]-2), 4, 4, linewidth=1, edgecolor='r', facecolor='none', label="Start Point")
    # ax.add_patch(rect)

    # plot DNet trajectory
    # dnet_data = np.genfromtxt("/home/xuefeng/Abs-DSO/build/logs/dnetlog.csv", delimiter=",", skip_header=1)
    # dnet_x = dnet_data[:,3]
    # dnet_y = dnet_data[:,5]
    # ax.plot(dnet_x, dnet_y, label="神经网络", linewidth=1)

    # plot ORB-SLAM trajectory
    # mono_orb_data = np.loadtxt("/home/xuefeng/data/kitti_odom/sequences/00/ORB_mono.txt")
    # mono_orb_x = mono_orb_data[:, 1]
    # mono_orb_y = mono_orb_data[:, 3]
    # ax.plot(mono_orb_x[:-150], mono_orb_y[:-150], label="单目ORB-SLAM", linewidth=1)

    # plot marginalization
    # use_HM_data = np.loadtxt("/mnt/sdb/xuefeng/kitti_odom/sequences/00/marginalization/HM/result.txt")
    # use_HM_x = use_HM_data[:, 1]
    # use_HM_y = use_HM_data[:, 3]
    # ax.plot(use_HM_x, use_HM_y, label="使用先验矩阵", color='r', linewidth=1)
    # reset_HM_data = np.loadtxt("/mnt/sdb/xuefeng/kitti_odom/sequences/00/marginalization/reset_HM/result.txt")
    # reset_HM_x = reset_HM_data[:, 1]
    # reset_HM_y = reset_HM_data[:, 3]
    # ax.plot(reset_HM_x, reset_HM_y, label="重置先验矩阵", color='g', linewidth=1)

    ax.grid()
    ax.axis("equal")
    ax.set_xlabel("X(m)")
    ax.set_ylabel("Y(m)")
    ax.legend(prop=legendfont)
    fig.savefig(f"{result_dir}.png", bbox_inches='tight', dpi=300)


if __name__ == "__main__":
    plot("15", "3_25_jixieguan_3")
    plot("16", "3_25_pengyuan_1")
    plot("17", "3_25_yangwangxingkong_1")
    plot("18", "3_26_jixieguan_1")
    plot("19", "3_26_jixieguan_2")
    plot("20", "3_26_jixieguan_3")
    plot("21", "3_26_yangwangxingkong_1")
