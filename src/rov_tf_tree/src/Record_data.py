#!/usr/bin/env python

import rospy
import rosbag
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from mavros_msgs.msg import Mavlink
import message_filters as mef

raw_imu_bag="/home/alineitudor/Licenta-git/BagFiles/IMU and Odom/ROV_raw_imu_data.bag"
preprocessed_imu_bag="/home/alineitudor/Licenta-git/BagFiles/IMU and Odom/DummyIMU.bag"
raw_bar_sensor_bag="/home/alineitudor/Licenta-git/BagFiles/IMU and Odom/raw_Bar30.bag"
depth_odom_bag="/home/alineitudor/Licenta-git/BagFiles/IMU and Odom/Depth_odom.bag"

all_in_one_bag="/home/alineitudor/Licenta-git/BagFiles/IMU and Odom/all_topics.bag"

def record(raw_imu_data,raw_Bar30_data,preproc_imu_data,depth_data):
    pass


if __name__=="__main__":
    sub_preproc_imu=mef.Subscriber('/BlueROV2/dummyBiasIMU',Imu)
    sub_raw_imu=mef.Subscriber('/BlueROV2/imu/data',Imu)
    sub_raw_Bar30=mef.Subscriber('/mavlink/from',Mavlink)
    sub_odom_depth=mef.Subscriber('/BlueRov2/odom/depth',Odometry)

    subs_list=[sub_raw_imu,sub_raw_Bar30,sub_preproc_imu,sub_odom_depth]
    all_topics=mef.TimeSynchronizer(subs_list,queue_size=100)
    all_topics.registerCallback(record)
    rospy.spin()

