cd ~/Abs-DSO/build
CUDA_VISIBLE_DEVICES=1 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/01/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/01/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/01/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/02/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/02/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/02/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/03/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/03/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/03/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/04/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/04/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/04/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/05/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/05/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/05/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/06/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/06/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/06/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/07/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/07/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/07/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/08/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/08/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/08/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/09/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/09/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/09/Trajectory.txt
CUDA_VISIBLE_DEVICES=0 bin/run_data files=/mnt/sdb/xuefeng/kitti_odom/sequences/cropped/10/image_2 calib=/mnt/sdb/xuefeng//kitti_odom/sequences/10/camera_rgb.txt preset=0 mode=1 nogui=1 nomt=1
cp Trajectory.txt /mnt/sdb/xuefeng/kitti_odom/sequences/cropped/10/Trajectory.txt