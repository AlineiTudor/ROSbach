#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

odom_filtered=Imu()
pub=rospy.Publisher('/repost/odometry',Imu)


def republish_changed_id(data):
    #odom_filtered=data
    #odom_filtered.header.frame_id="pixhawk_frame"
    pub.publish(data)

    rospy.loginfo(data)
    #rospy.loginfo(rospy.get_caller_id()+": Pose: %s;\tTwist: %s",data.pose,data.twist)

if __name__=="__main__":
    rospy.init_node("reading_odometry",anonymous=True)
    rospy.Subscriber("/BlueRov2/imu/data",Imu,republish_changed_id)
    rospy.spin()
    