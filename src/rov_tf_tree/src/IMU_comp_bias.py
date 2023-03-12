#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

def NED2ENU_second(measurement):
    acc_x_aux=measurement.linear_acceleration.x
    measurement.linear_acceleration.x=measurement.linear_acceleration.y
    measurement.linear_acceleration.y=acc_x_aux
    measurement.linear_acceleration.z*=-1

    ang_vel_x=measurement.angular_velocity.x
    measurement.angular_velocity.x=measurement.angular_velocity.y
    measurement.angular_velocity.y=ang_vel_x
    measurement.angular_velocity.z=-measurement.angular_velocity.z
    
    
    aux_orient_x= measurement.orientation.x
    measurement.orientation.x=measurement.orientation.y
    measurement.orientation.y=aux_orient_x
    measurement.orientation.z*=-1

    return measurement

subscriber_name="raw_imu_reader"
subscriber_topic="/BlueRov2/imu/data"

publisher_name="corrected_imu_publisher"
publisher_topic="/BlueROV2/dummyBiasIMU"

flag=False
display1_flag=True
usr_in="none"
bias={"acc_x":0,"acc_y":0,"samples":0}
time=10#sec
first_sample_time=rospy.Time()
bias_mean={"x":0,"y":0}

variance_acc=1
variance_ang_vel=0.1
variance_orient=0.1
linear_acc_cov=[variance_acc, 0, 0,0,variance_acc,0,0,0,variance_acc]
ang_vel_cov=[variance_ang_vel,0,0,0,variance_ang_vel,0,0,0,variance_ang_vel]
orient_cov=[variance_orient,0,0,0,variance_orient,0,0,0,variance_orient]

pub=rospy.Publisher(publisher_topic,Imu,queue_size=100)

def repostIMUdata(data):
    global display1_flag,flag,bias,bias_mean,first_sample_time
    if display1_flag:
        first_sample_time=rospy.Time.now()
        rospy.loginfo("DO NOT MOVE ROBOT WHILE MEASURING BIAS")
        display1_flag=False
    duration=rospy.Time.now()-first_sample_time
    if duration.to_sec()<=time:#Recorded 10 seconds of static acceleration
        bias["acc_x"]+=data.linear_acceleration.x
        bias["acc_y"]+=data.linear_acceleration.y
        bias["samples"]+=1
    elif flag==False: 
        bias_mean["x"]=bias["acc_x"]/bias["samples"]
        bias_mean["y"]=bias["acc_y"]/bias["samples"]
        flag=True
        rospy.loginfo("Bias mean computed: %s.\nReposting IMU data....",bias_mean)
    if flag:
        data.linear_acceleration.x-=bias_mean["x"]
        data.linear_acceleration.y-=bias_mean["y"]
        data=NED2ENU_second(data)
        data.linear_acceleration_covariance=linear_acc_cov
        data.angular_velocity_covariance=ang_vel_cov
        data.orientation_covariance=orient_cov
        data.header.frame_id="pixhawk"
        pub.publish(data)
              

    

if __name__=="__main__":
    
    rospy.init_node(subscriber_name,anonymous=True)
    rospy.Subscriber(subscriber_topic,Imu,repostIMUdata,queue_size=1000)
    rospy.loginfo("%s started reading from %s",subscriber_name,subscriber_topic)
    rospy.loginfo("Started reading IMU.....")
    rospy.spin()