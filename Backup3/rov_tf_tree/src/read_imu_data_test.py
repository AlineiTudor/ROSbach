#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu


def readImuData(data):
    #rospy.loginfo("Orientation covariance: %s",data.orientation_covariance)
    #rospy.loginfo("Angular velocity cov: %s",data.angular_velocity_covariance)
    #rospy.loginfo("Linear acc cov: %s",data.linear_acceleration_covariance)
    rospy.loginfo("Angular velocity:\n %s",data.angular_velocity)
    rospy.loginfo("Orientation:\n %s",data.orientation)
    rospy.loginfo("Linear acceleration:\n %s",data.linear_acceleration)
    rospy.loginfo("\n\n")
    

if __name__=="__main__":
    rospy.init_node("reading_imu_test",anonymous=True)
    rospy.Subscriber("/BlueRov2/imu/data",Imu,readImuData)
    rospy.loginfo("Started reading IMU....")
    rospy.spin()
