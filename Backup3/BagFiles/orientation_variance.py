#!/usr/bin/env python


import rosbag
import numpy as np
import rospy
import math
import json as js



bagInName="/home/alineitudor/Licenta/BagFiles/IMU_and_depth/deviatie_orientare2.bag"#varianta_orientare1.bag"
bagin=rosbag.Bag(bagInName)

def ToEulerAngles(q):

    # roll (x-axis rotation)
    sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
    cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
    roll =math.atan2(sinr_cosp, cosr_cosp)
    # pitch (y-axis rotation)
    sinp = math.sqrt(1 + 2 * (q.w * q.y - q.x * q.z))
    cosp = math.sqrt(1 - 2 * (q.w * q.y - q.x * q.z))
    pitch = 2 * math.atan2(sinp, cosp) - math.pi / 2

    # yaw (z-axis rotation)
    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return (math.degrees(roll),math.degrees(pitch),math.degrees(yaw))

mean={"r":0,"p":0,"y":0}
samples=0
angles=[]
for topic, msg, t in bagin:
    if topic=="/BlueROV2/dummyBiasIMU":
       q = msg.orientation
       samples+=1
       orientation_list = [q.x, q.y, q.z, q.w]
       ang = ToEulerAngles(q)
       angles.append(ang)
       mean["r"]+=ang[0]
       mean["p"]+=ang[1]
       mean["y"]+=ang[2]
bagin.close()

mean["r"]/=samples
mean["p"]/=samples
mean["y"]/=samples
#print(mean)
dif=[0,0,0]
for i in range(len(angles)):
    dif[0]+=(angles[i][0]-mean["r"])**2
    dif[1]+=(angles[i][1]-mean["p"])**2
    dif[2]+=(angles[i][2]-mean["y"])**2

deviation={"r":math.sqrt(dif[0]/samples),"p":math.sqrt(dif[1]/samples),"y":math.sqrt(dif[2]/samples)}
#print(deviation)
f=open("/home/alineitudor/Licenta/BagFiles/IMU_and_depth/deviatie_orientare.txt","w")
f.write(f"samples: {samples}\n")
f.write(f"mean (roll, pitch, yaw): {js.dumps(mean)}\n")
f.write(f"standard deviation (roll, pitch, yaw): {js.dumps(deviation)}\n")
f.close()

