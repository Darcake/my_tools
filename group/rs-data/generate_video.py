import os

import cv2
from tqdm import tqdm


def main():
    ws_dir = "/home/xuefeng/dataset/tongji_odom/20201206"
    img_dir = os.path.join(ws_dir, "image_0")
    # img_dir = os.path.join(ws_dir, "images_dum")
    # img_dir = "/home/wzy/DNet/disps_odom_tongji/"
    # save_file = "video.avi"
    save_file = os.path.join(ws_dir, "video_0.avi")

    fps = 15
    size = (640, 192)
    # size = (640, 192)
    vw = cv2.VideoWriter(save_file, cv2.VideoWriter_fourcc('M','J','P','G'), fps, size)

    file_num = len([name for name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, name))])
    # for i in tqdm(range(file_num)):
    for i in tqdm(range(452)):
        img_file = os.path.join(img_dir, "{:0>6d}.png".format(i))
        img = cv2.imread(img_file)
        vw.write(img)   
    vw.release()


if __name__ == "__main__":
    main()