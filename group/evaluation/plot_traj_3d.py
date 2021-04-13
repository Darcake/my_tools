import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 6})
plt.rcParams["font.family"] = "Times New Roman"
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation


def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # plot Stereo DSO trajectory
    # stereo_data = np.loadtxt("result_stereo.txt")
    # stereo_x = stereo_data[:,1]
    # stereo_y = stereo_data[:,2]
    # stereo_z = stereo_data[:,3]
    # ax.plot(stereo_x, stereo_z, stereo_y, label="Stereo DSO", linewidth=1)

    # plot Stereo DSO coarse tracking trajectory
    # stereo_ct_data = np.loadtxt("coarseTrackingLog.txt")
    # stereo_ct_x = stereo_ct_data[:,3]
    # stereo_ct_y = stereo_ct_data[:,4]
    # stereo_ct_z = stereo_ct_data[:,5]
    # ax.plot(stereo_ct_x, stereo_ct_z, stereo_ct_y, label="Coarse Tracking", linewidth=1)

    # plot Abs DSO trajectory
    # abs_data = np.loadtxt("/home/xuefeng/Abs-DSO/build/result.txt")
    # abs_x = abs_data[:,1]
    # abs_y = abs_data[:,2]
    # abs_z = abs_data[:,3]
    # ax.plot(abs_x, abs_z, -abs_y, label="Abs DSO", linewidth=1)

    # plot Abs DSO coarse tracking trajectory
    ct_data = np.genfromtxt("/home/xuefeng/Abs-DSO/build/logs/trackinglog.csv", delimiter=",", skip_header=1)
    ct_x = ct_data[:,4]
    ct_y = ct_data[:,5]
    ct_z = ct_data[:,6]
    ax.plot(ct_x, ct_z, ct_y, label="Coarse Tracking", linewidth=1)
    idx = 178
    ax.plot(ct_x[idx], ct_z[idx], ct_y[idx], marker='o', markersize=1)

    ax.legend()
    fig.savefig("traj_3d.png", bbox_inches='tight', dpi=300)
    plt.show()


if __name__ == "__main__":
    main()