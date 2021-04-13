import os
from shutil import copyfile

from cv2 import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def crop_img(raw_dir, ws_dir, raw_name, ws_name, idx, crop_u, crop_v, crop_h, crop_w):
    img_folder = "image_{}".format(idx)
    img_dir = os.path.join(raw_dir, raw_name, "images_1", img_folder)
    save_dir = os.path.join(ws_dir, ws_name, img_folder)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_num = len([name for name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, name))])
    print("=> cropping images in {}, crop_u: {}, crop_v: {}, crop_h: {}, crop_w: {}".format(
        img_dir, crop_u, crop_v, crop_h, crop_w
    ))
    for i in tqdm(range(file_num)):
        img_file = os.path.join(img_dir, "{:0>6d}.png".format(i))
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

def func(raw_dir:"需要裁剪的图片的路径", name:"str,需要裁剪的图片的下一级文件夹名称", ws_dir:"str,裁剪后图像的保存路径", num:"str,裁剪后图像的保存的下一级文件夹名称", idx:"int,裁剪图片的索引", crop_v:"int,y方向上裁剪尺寸"):
    crop_img(raw_dir, ws_dir, name, num, idx, 0, crop_v, 192, 640)
    generate_video(ws_dir, num, idx)
    copyfile(os.path.join(raw_dir, name, "gps_data.txt"), os.path.join(ws_dir, num, "gnss.txt"))
    copyfile(os.path.join(raw_dir, name, "cam_info_1.txt"), os.path.join(ws_dir, num, "cam_info.txt"))


def main():
    raw_dir = "D:/data/zx_2"
    ws_dir = "D:/data/zx_3"
    if not os.path.exists(ws_dir):
        os.makedirs(ws_dir)

    func(raw_dir, "3_25_jixieguan_1", ws_dir, "13", 0, 151)    
    func(raw_dir, "3_25_jixieguan_2", ws_dir, "14", 0, 151)
    func(raw_dir, "3_25_jixieguan_3", ws_dir, "15", 0, 153)
    func(raw_dir, "3_25_pengyuan_1", ws_dir, "16", 0, 152)
    func(raw_dir, "3_25_yangwangxingkong_1", ws_dir, "17", 0, 155)
    func(raw_dir, "3_26_jixieguan_1", ws_dir, "18", 0, 153)
    func(raw_dir, "3_26_jixieguan_2", ws_dir, "19", 0, 149)
    func(raw_dir, "3_26_jixieguan_3", ws_dir, "20", 0, 151)
    func(raw_dir, "3_26_yangwangxingkong_1", ws_dir, "21", 0, 156)

    # time_sync(raw_dir, ws_dir)


if __name__ == "__main__":
    main()
