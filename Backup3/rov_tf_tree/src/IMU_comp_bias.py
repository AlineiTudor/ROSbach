#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from tf.transformations import *
from geometry_msgs.msg import Quaternion,Vector3,Transform,Vector3Stamped
import json
#import tf2_geometry_msgs.tf2_geometry_msgs as tf2




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
#subscriber_topic="/BlueRov2/imu/data"
subscriber_topic='/mavros/imu/data'

publisher_name="corrected_imu_publisher"
publisher_topic="/BlueROV2/dummyBiasIMU"

flag=False
display1_flag=True
usr_in="none"
bias={"acc_x":0,"acc_y":0,"acc_z":0,"samples":0}
time=10#sec
first_sample_time=rospy.Time()
bias_mean={"x":0,"y":0,"z":0}

variance_acc=0.003
variance_ang_vel=0.04
variance_orient=0.1
linear_acc_cov=[variance_acc, 0, 0,0,variance_acc,0,0,0,variance_acc]
ang_vel_cov=[variance_ang_vel,0,0,0,variance_ang_vel,0,0,0,variance_ang_vel]
orient_cov=[variance_orient,0,0,0,variance_orient,0,0,0,variance_orient]

pub=rospy.Publisher(publisher_topic,Imu,queue_size=100)


def remove_gravit_acc(data):
    quat=[data.orientation.w,data.orientation.x,data.orientation.y,data.orientation.z]
    #quat=[data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w]
    imu_acc=[data.linear_acceleration.x,data.linear_acceleration.y,data.linear_acceleration.z]
    #check which one gives better results->constant g or z acc from imu
    g_ct=9.8
    #g_ct=data.linear_acceleration.z
    g=[0,0,0]
    new_acc=[0.0,0.0,0.0]
    g[0]=2*(quat[1]*quat[3]-quat[0]*quat[2])
    g[1]=2*(quat[0]*quat[1]+quat[2]*quat[3])
    g[2]=quat[0]**2-quat[1]**2-quat[2]**2+quat[3]**2
    
    #removing gravit from acceleraion
    new_acc[0]=imu_acc[0]-g[0]*g_ct
    new_acc[1]=imu_acc[1]-g[1]*g_ct
    new_acc[2]=imu_acc[2]-g[2]*g_ct
    return new_acc

def remove_gravit_acc2(data):
    g_ct=9.8066#*****
    g_comp=[0,0,g_ct,0]
    #g_ct=data.linear_acceleration.z

    imu_acc_quat=[data.linear_acceleration.x,data.linear_acceleration.y,data.linear_acceleration.z,0]
    #f = open("/home/alineitudor/Licenta/BagFiles/IMU_and_depth/acc_meas.txt", "a")
    #f.write(str(imu_acc_quat)+"\n")
    #f.close()


    orient=[data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w]
    orient_inv=quaternion_inverse(orient)
    
    #(1) 
    #rotating gravity to local frame
    acc_proj=quaternion_multiply(orient_inv,g_comp)
    acc_proj=quaternion_multiply(acc_proj,quaternion_conjugate(orient_inv))
    #f = open("/home/alineitudor/Licenta/BagFiles/IMU_and_depth/acc_proj.txt", "a")
    #f.write(str(acc_proj)+"\n")
    #f.close()



    #(2)
    #acc_proj=quaternion_multiply(orient,imu_acc_quat)
    #acc_proj=quaternion_multiply(acc_proj,quaternion_conjugate(orient))
    #acc_proj[2]-=g_comp[2]
    #acc_proj=quaternion_multiply(orient_inv,acc_proj)
    #acc_proj=quaternion_multiply(acc_proj,quaternion_conjugate(orient_inv))

    #(2)
    #return acc_proj
    #(1)
    #substracting gravity projection in local frame from local acceleration to get pure x,y,z accelerations
    result=[imu_acc_quat[0]-acc_proj[0],imu_acc_quat[1]-acc_proj[1],imu_acc_quat[2]-acc_proj[2]]
    #f = open("/home/alineitudor/Licenta/BagFiles/IMU_and_depth/biases.txt", "a")
    #f.write(str(result)+"\n")
    #f.close()

    return result


def repostIMUdata(data):
    global display1_flag,flag,bias,bias_mean,first_sample_time
    if display1_flag:
        first_sample_time=rospy.Time.now()
        rospy.loginfo("DO NOT MOVE ROBOT WHILE MEASURING BIAS")
        display1_flag=False
    duration=rospy.Time.now()-first_sample_time
    if duration.to_sec()<=time:#Recorded 10 seconds of static acceleration
        #new_acc=remove_gravit_acc(data)
        new_acc=remove_gravit_acc2(data)
        bias["acc_x"]+=new_acc[0]#data.linear_acceleration.x
        bias["acc_y"]+=new_acc[1]#data.linear_acceleration.y
        bias["acc_z"]+=new_acc[2]#data.linear_acceleration.z
        bias["samples"]+=1
    elif flag==False: 
        bias_mean["x"]=bias["acc_x"]/bias["samples"]
        bias_mean["y"]=bias["acc_y"]/bias["samples"]
        bias_mean["z"]=bias["acc_z"]/bias["samples"]
        flag=True
        f = open("/home/alineitudor/Licenta/BagFiles/IMU_and_depth/bias.txt", "w")
        f.write(json.dumps(bias_mean))
        f.close()
        rospy.loginfo("Bias mean computed: %s.\nReposting IMU data....",bias_mean)
    if flag:
        data.linear_acceleration.x-=bias_mean["x"]
        data.linear_acceleration.y-=bias_mean["y"]
        data.linear_acceleration.z-=bias_mean["z"]
        #data=NED2ENU_second(data)
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