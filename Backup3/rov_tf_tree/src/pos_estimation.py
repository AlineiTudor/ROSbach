#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

def callback(data):
    rospy.loginfo(rospy.get_caller_id()+": Pose: %s;\tTwist: %s",data.pose,data.twist)

if __name__=="__main__":
    rospy.init_node("reading_odometry",anonymous=True)
    rospy.Subscriber("/BlueRov2/odometry",Odometry,callback)
    rospy.loginfo("Started reading odometry.....")
    rospy.spin()
