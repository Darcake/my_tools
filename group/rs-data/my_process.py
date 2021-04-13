import os
from shutil import copyfile

from cv2 import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def crop_img(raw_dir, ws_dir, raw_name, ws_name, idx, crop_u, crop_v, crop_h, crop_w):
    img_folder = f"image_{idx}"
    raw_dir = os.path.join(raw_dir, raw_name, img_folder)
    save_dir = os.path.join(ws_dir, ws_name, img_folder)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_num = len([name for name in os.listdir(raw_dir) if os.path.isfile(os.path.join(raw_dir, name))])
    print("=> cropping images in {}, crop_u: {}, crop_v: {}, crop_h: {}, crop_w: {}".format(
        raw_dir, crop_u, crop_v, crop_h, crop_w
    ))
    for i in tqdm(range(file_num)):
        img_file = os.path.join(raw_dir, "{:0>6d}.png".format(i))
        img = cv2.imread(img_file)
        cropped = img[crop_v:crop_v+crop_h,crop_u:crop_u+crop_w]
        save_file = os.path.join(save_dir, "{:0>6d}.png".format(i))
        cv2.imwrite(save_file, cropped)


def time_sync(raw_dir, ws_dir):
    img_info_raw  = np.loadtxt(os.path.join(raw_dir, "cam_info.txt"))
    gnss_info_raw = np.loadtxt(os.path.join(raw_dir, "gnss.txt"))
    gnss_info_sync = []
    for i in range(img_info_raw.shape[0]):
        idx = np.abs(gnss_info_raw[:,0] - img_info_raw[i,0]).argmin()
        gnss_info_sync.append(gnss_info_raw[idx])
    gnss_info_sync = np.array(gnss_info_sync)
    np.savetxt(os.path.join(ws_dir, "gnss_sync.txt"), gnss_info_sync, fmt="%d %d %s %s %s %s %s %s %d")


def generate_video(ws_dir, ws_name, idx):
    img_folder = "image_{}".format(idx)
    img_dir = os.path.join(ws_dir, ws_name, img_folder)
    video_name = "video_{}.avi".format(idx)
    save_file = os.path.join(ws_dir, ws_name, video_name)
    fps = 30
    size = (640, 192)
    vw = cv2.VideoWriter(save_file, cv2.VideoWriter_fourcc('M','J','P','G'), fps, size)
    file_num = len([name for name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, name))])
    print("=> generating video: {}".format(save_file))
    for i in tqdm(range(file_num)):
        img_file = os.path.join(img_dir, "{:0>6d}.png".format(i))
        img = cv2.imread(img_file)
        vw.write(img)   
    vw.release()


def func(raw_dir:"需要裁剪的图片的路径", raw_name:"str,需要裁剪的图片的下一级文件夹名称", ws_dir:"str,裁剪后图像的保存路径", ws_name:"str,裁剪后图像的保存的下一级文件夹名称", idx:"int,裁剪图片的索引", crop_u:"int,x方向上裁剪尺寸", crop_v:"int,y方向裁剪的尺寸", crop_h:"int,裁剪后图片的y尺寸", crop_w:"int，裁剪后图片的x尺寸"):
    crop_img(raw_dir, ws_dir, raw_name, ws_name, idx, crop_u, crop_v, crop_h, crop_w)
    # generate_video(ws_dir, ws_name, idx)
    # copyfile(os.path.join(raw_dir, name, "gps_data.txt"), os.path.join(ws_dir, num, "gnss.txt"))
    # copyfile(os.path.join(raw_dir, name, "cam_info_1.txt"), os.path.join(ws_dir, num, "cam_info.txt"))


def main():
    raw_dir = "/mnt/sdb/xuefeng/kitti_odom/sequences"
    ws_dir = "/mnt/sdb/xuefeng/kitti_odom/sequences/cropped"
    if not os.path.exists(ws_dir):
        os.makedirs(ws_dir)

    # 需要裁剪的图片的路径格式：raw_dir->raw_name->image_{idx};裁剪后图片的保存路径：ws_dir->ws_name->image_{idx}
    func(raw_dir, "01", ws_dir, "01", 2, 25, 4, 352, 1216) # 本来是要截取38，但不够   
    func(raw_dir, "02", ws_dir, "02", 2, 25, 5, 352, 1216)  # 本来是要截取25
    func(raw_dir, "03", ws_dir, "03", 2, 26, 23, 352, 1216)  # 本来要截取37
    func(raw_dir, "04", ws_dir, "04", 2, 10, 8, 352, 1216) # 本来要截取48
    func(raw_dir, "05", ws_dir, "05", 2, 10, 18, 352, 1216) # 本来要截取37
    func(raw_dir, "06", ws_dir, "06", 2, 10, 10, 352, 1216)  # 本来要截取35
    func(raw_dir, "07", ws_dir, "07", 2, 10, 5, 352, 1216) # 本来要截取39
    func(raw_dir, "08", ws_dir, "08", 2, 10, 2, 352, 1216)  # 本来要截取45
    func(raw_dir, "09", ws_dir, "09", 2, 10, 0, 352, 1216)  # 本来要截取29
    func(raw_dir, "10", ws_dir, "10", 2, 1, 8, 352, 1216)


    # time_sync(raw_dir, ws_dir)


if __name__ == "__main__":
    main()
