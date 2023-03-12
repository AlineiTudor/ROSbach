import numpy as np
"""
a=[0, 0, 0]
a=np.array([1,2,3])+np.array([2,3 ,4])
print(a/2)
a=[[0, 0, 0],[0,0,0],[0,0,0]]
print([x for x1 in a for x in x1])
"""
#import rosbag

'''
bagin=rosbag.Bag("/home/alineitudor/Licenta/BagFiles/Circle2Cov.bag")
#print(bag)
times=0
test=False
for a,b,c in bagin.read_messages(topics=['/BlueRov2/imu/data']):
    print(b.linear_acceleration.x)
    for x in b.linear_acceleration_covariance:
        if x!=0:
            times+=1
            print(b)
            test=True
            break
    if test and times==100000:
        break'''

"""
a=[1, 0.2, 3.3, 1, 9]
for i in range(len(a)):
    print(a[i])
"""
"""
c=(2,1)
print(len(c))

import struct as st

n=st.pack('hh',32768-1,1)
print(n)
m=st.unpack('hxx',n)
print(m)
c="a"
b="a"
print(c==b)

def ceva(c):
    print(c)


import keyboard


a=keyboard.record(" ")
while True:
    if a==" ":
        print("good")
        break
"""

x=1

def fct():
    global x
    x+=1
    a=x.bit_length
    print(a)
fct()
print(x)

from geometry_msgs.msg import Point,Pose,Quaternion,Twist,Vector3

quat=Quaternion()
print(quat)

from nav_msgs.msg import Odometry
od=Odometry()
print(od)