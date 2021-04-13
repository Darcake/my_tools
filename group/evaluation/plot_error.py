from math import pi,cos,sin

import numpy as np
from scipy.spatial.transform import Rotation
from pyproj import Transformer
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams.update({'font.size': 6})
plt.rcParams["font.family"] = "Times New Roman"

song = FontProperties(fname='/usr/share/fonts/truetype/windows-font/simsun.ttc', size=6)
fontcn = {'fontproperties': song, 'size': 6, 'weight': 'normal'}
legendfont = FontProperties(fname='/usr/share/fonts/truetype/windows-font/simsun.ttc', size=6)


def add_homo(T):
    homo = np.expand_dims(np.tile(np.array([0, 0, 0, 1]), (T.shape[0], 1)), axis=1)
    T = np.concatenate([T, homo], axis=1)
    return T


def transform_global2local(T):
    list_local_T = []
    for i in range(T.shape[0]-1):
        local_T = np.linalg.inv(T[i]) @ T[i+1]
        list_local_T.append(np.expand_dims(local_T, axis=0))
    np_local_T = np.concatenate(list_local_T, axis=0)
    return np_local_T


def transform_local2global(T):
    global_T = np.eye(4)
    list_global_T = [np.expand_dims(global_T, axis=0)]
    for i in range(T.shape[0]):
        global_T = global_T @ T[i]
        list_global_T.append(np.expand_dims(global_T, axis=0))
    np_global_T = np.concatenate(list_global_T, axis=0)
    return np_global_T


def transform_quaternion2T(quaternion, t):
    t = np.expand_dims(t, axis=2)
    R = Rotation.from_quat(quaternion).as_matrix()
    T = np.concatenate([R, t], axis=2)
    T = add_homo(T)
    return T


def transform_euler2T(euler, t):
    t = np.expand_dims(t, axis=2)
    R = Rotation.from_euler("xyz", euler, degrees=True).as_matrix()
    T = np.concatenate([R, t], axis=2)
    T = add_homo(T)
    return T


def transform_T2euler(T):
    t = T[:, :3, 3]
    euler = Rotation.from_matrix(T[:, :3, :3]).as_euler("yxz", degrees=True)
    return euler, t


def rotate_xy(x, y, heading, degree=True):
    if degree == True:
        heading = heading * pi / 180
    rotate_x = np.copy(x) * cos(heading) - np.copy(y) * sin(heading)
    rotate_y = np.copy(x) * sin(heading) + np.copy(y) * cos(heading)
    return rotate_x, rotate_y


def calculate_error(data, gt):
    lon = data[:,2,3]
    lat = data[:,0,3]
    gt_lon = gt[:,2,3]
    gt_lat = gt[:,0,3]
    lon_error = lon - gt_lon
    lat_error = lat - gt_lat
    return lon_error, lat_error


def rmse(error):
    return np.sqrt(np.mean(error**2))


def main():
    x = np.linspace(0, 999, 999)
    # x = np.linspace(0, 300, 300)
    fig = plt.figure(figsize=(3, 3))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)

    # TiEV GNSS data
    # gt = np.loadtxt("/home/xuefeng/data/tiev_odom/04/gnss_sync_0.txt", usecols=[0,1,2,3])
    # lat = gt[:,1]
    # lon = gt[:,2]
    # heading = gt[:,3] / pi * 180
    # heading = heading - heading[0]
    # transformer = Transformer.from_crs("epsg:4326", "epsg:32651")
    # utm_x, utm_y = transformer.transform(lat, lon)
    # utm_x = utm_x - utm_x[0]
    # utm_y = utm_y - utm_y[0]
    # utm_x = utm_x[abs(utm_x) < 1000]
    # utm_y = utm_y[abs(utm_y) < 1000]
    # rotate_utm_x, rotate_utm_y = rotate_xy(utm_x, utm_y, -24)
    # zeros = np.zeros_like(lat)
    # gt_euler = np.stack([zeros, -heading, zeros], axis=1)
    # gt_t = np.stack([rotate_utm_x, zeros, rotate_utm_y], axis=1)
    # gt_T = transform_euler2T(gt_euler, gt_t)
    # gt_T = gt_T[:300]
    # gt_euler = gt_euler[:300]
    # gt_T_inc = transform_global2local(gt_T)
    
    # KITTI data
    gt = np.loadtxt("/mnt/sdb/xuefeng/kitti_odom/poses/00.txt")
    gt_T = np.reshape(gt, (gt.shape[0], 3, 4))
    gt_T = add_homo(gt_T)
    gt_T = gt_T[:1000]
    gt_T_inc = transform_global2local(gt_T)

    # DSO data
    dso_data = np.loadtxt("/home/xuefeng/dso/build/result.txt")
    dso_t = dso_data[:1000, 1:4]
    dso_quaternion = dso_data[:1000, 4:]
    dso_T = transform_quaternion2T(dso_quaternion, dso_t)
    dso_T_inc = transform_global2local(dso_T)
    dso_lon_error, dso_lat_error = calculate_error(dso_T_inc, gt_T_inc)
    ax1.plot(x[7:], dso_lat_error[7:], label="改进前算法", color='r', linewidth=1)
    ax2.plot(x[7:], dso_lon_error[7:], label="改进前算法", color='r', linewidth=1)
    print("DSO RMSE: {}, {}".format(rmse(dso_lat_error[7:]), rmse(dso_lon_error[7:])))

    # Stereo DSO data
    # stereo_data = np.loadtxt("/home/xuefeng/stereo_dso/build/result.txt")
    # stereo_T = np.reshape(stereo_data, (stereo_data.shape[0], 3, 4))
    # stereo_T = add_homo(stereo_T)
    # stereo_T_inc = transform_global2local(stereo_T)
    # stereo_lon_error, stereo_lat_error = calculate_error(stereo_T_inc, gt_T_inc)
    # ax1.plot(x, stereo_lat_error, label="双目DSO", color='r', linewidth=1)
    # ax2.plot(x, stereo_lon_error, label="双目DSO", color='r', linewidth=1)
    # print("Stereo DSO RMSE: {}, {}".format(rmse(stereo_lat_error), rmse(stereo_lon_error)))

    # Abs DSO data
    abs_data = np.loadtxt("/home/xuefeng/data/kitti_odom/sequences/00/result/result.txt")
    # abs_data = np.genfromtxt("/home/xuefeng/data/tiev_odom/04/result/result.csv", delimiter=",", skip_header=1)
    abs_t = abs_data[:, 1:4]
    abs_quaternion = abs_data[:, 4:]
    abs_T = transform_quaternion2T(abs_quaternion, abs_t)
    abs_T_inc = transform_global2local(abs_T)
    abs_lon_error, abs_lat_error = calculate_error(abs_T_inc, gt_T_inc)
    ax1.plot(x, abs_lat_error, label="改进后算法", color='b', linewidth=1)
    ax2.plot(x, abs_lon_error, label="改进后算法", color='b', linewidth=1)
    print("Abs DSO RMSE: {}, {}".format(rmse(abs_lat_error), rmse(abs_lon_error)))    

    # Abs DSO marginalization
    # use_HM_data = np.loadtxt("/mnt/sdb/xuefeng/kitti_odom/sequences/00/marginalization/HM/result.txt")
    # use_HM_t = use_HM_data[:, 1:4]
    # use_HM_quaternion = use_HM_data[:, 4:]
    # use_HM_T = transform_quaternion2T(use_HM_quaternion, use_HM_t)
    # use_HM_T_inc = transform_global2local(use_HM_T)
    # use_HM_lon_error, use_HM_lat_error = calculate_error(use_HM_T_inc, gt_T_inc)
    # ax1.plot(x, use_HM_lat_error, label="使用先验矩阵", color='r', linewidth=1)
    # ax2.plot(x, use_HM_lon_error, label="使用先验矩阵", color='r', linewidth=1)
    # print("Use HM RMSE: {}, {}".format(rmse(use_HM_lat_error), rmse(use_HM_lon_error)))    
    # reset_HM_data = np.loadtxt("/mnt/sdb/xuefeng/kitti_odom/sequences/00/marginalization/reset_HM/result.txt")
    # reset_HM_t = reset_HM_data[:, 1:4]
    # reset_HM_quaternion = reset_HM_data[:, 4:]
    # reset_HM_T = transform_quaternion2T(reset_HM_quaternion, reset_HM_t)
    # reset_HM_T_inc = transform_global2local(reset_HM_T)
    # reset_HM_lon_error, reset_HM_lat_error = calculate_error(reset_HM_T_inc, gt_T_inc)
    # ax1.plot(x, reset_HM_lat_error, label="重置先验矩阵", color='g', linewidth=1)
    # ax2.plot(x, reset_HM_lon_error, label="重置先验矩阵", color='g', linewidth=1)
    # print("Reset HM RMSE: {}, {}".format(rmse(reset_HM_lat_error), rmse(reset_HM_lon_error)))    

    ax1.set_xlim([0, x[:-1].shape[0]])
    ax1.set_ylabel("侧向误差(m)", fontproperties=song)
    ax1.set_xlabel("帧号", fontproperties=song)
    lines, labels = ax1.get_legend_handles_labels()
    # ax1.legend(prop=legendfont, loc="upper left", bbox_to_anchor=(1.0,0.75))
    ax1.grid()

    ax2.set_xlim([0, x[:-1].shape[0]])
    ax2.set_ylabel("纵向误差(m)", fontproperties=song)
    ax2.set_xlabel("帧号", fontproperties=song)
    # ax2.legend(prop=legendfont, loc="upper left", bbox_to_anchor=(1.0,0.75))
    ax2.grid()

    fig.legend(lines, labels, prop=legendfont, loc="center left", bbox_to_anchor=(0.3, 1.0), ncol=2)
    fig.tight_layout()
    fig.align_labels()

    plt.savefig("error.png", bbox_inches='tight', dpi=300)
    plt.close()


if __name__ == "__main__":
    main()
