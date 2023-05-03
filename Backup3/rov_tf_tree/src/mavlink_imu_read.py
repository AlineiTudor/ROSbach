#!/usr/bin/env python

import rospy
from struct import pack, unpack
import pymavlink
from mavros_msgs.msg import Mavlink
from nav_msgs.msg import Odometry
import tf2_ros
from geometry_msgs.msg import Point,Pose,Quaternion,Twist

#preparing publisher for tf
odom_broadcaster=tf2_ros.TransformBroadcaster()
tf_point=Point()
tf_pose=Pose()
tf_quat=Quaternion()
tf_quat.w=1
tf_twist=Twist()


publisher_name='depth_publisher'
publisher_topic='/BlueRov2/odom/depth'
flag=False#to loginfo that publisher started publishing

subscriber_name='Bar30_primary_listener'
subscriber_topic='/mavlink/from'
pub=rospy.Publisher(publisher_name,Odometry,queue_size=100)
###Odometry
odom_msg=Odometry()
depth=0
water_density=1000#kg/m^3 for fresh water
g=9.80675#[m/s^2] in Cluj-Napoca
z_covarince=[0]*36
z_covarince[14]=0.3
seq=1


def decode_info(data):
    global seq,odom_msg
    #raw imu 26
    #scaled imu 27,116,129
    if data.msgid==27:
        #pack=convert from C struct to Python values->QQ unsigned long long
        #p=pack("QQ",*data.payload64)
        #unpack value as unsigned int, floar, float and short

        ##Construct header
        #ceva=unpack("Iffhxx",p)
        rospy.loginfo("---------------")
        rospy.loginfo(data)
        rospy.loginfo("---------------")

def listener():
    rospy.init_node(subscriber_name,anonymous=True)
    rospy.Subscriber(subscriber_topic,Mavlink,decode_info)
    rospy.loginfo("%s started listening to mavlink imu....",subscriber_name)
    rospy.spin()

if __name__=="__main__":
    listener()