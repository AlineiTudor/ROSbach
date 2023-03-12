import rosbag
import numpy as np
import rospy
import math
#import tf.transformations as tr

#rot_90_z_quat=tr.quaternion_from_euler(0,0,math.pi/2)

bagInName="/home/alineitudor/Licenta/BagFiles/Square.bag"
bagOutName="/home/alineitudor/Licenta/BagFiles/Square2Cov.bag"
bagin=rosbag.Bag(bagInName)
bagout=rosbag.Bag(bagOutName,'w')

acc_noise=100*0.000001*9.89#(m/s^2)/sqrt(Hz)
#noise_bw=1100#1 sample avg
#noise_bw=442#4 sample avg
#noise_bw=236#8 sample avg
noise_bw=122#16 sample avg
#noise_bw=62#32 sample avg
variance=acc_noise*math.sqrt(noise_bw)
variance=variance*variance

n=0
x=[]
x_med=[]
Q=[]
sumQ=[[0, 0, 0],[0,0,0],[0,0,0]]
sumx_med=[0, 0, 0]
current_meas=[]
aux_diff=[]
for topic, msg, t in bagin:
    n+=1
    #print(type(msg.orientation))
    if n==1:#1674216802
        print(msg)
        bias=[msg.linear_acceleration.x, msg.linear_acceleration.y]
        #print(f"first measurement\n {msg}")
        #break
'''
    current_meas=[msg.linear_acceleration.x,msg.linear_acceleration.y,msg.linear_acceleration.z]

    sumx_med=np.array(sumx_med)+np.array(current_meas)
x_med=sumx_med/n
'''
bagin.close()

'''
bagin=rosbag.Bag(bagInName)
#t_prev=0
#periods=[]
for topic, msg,t in bagin:
    current_meas=[msg.linear_acceleration.x,msg.linear_acceleration.y,msg.linear_acceleration.z]
    aux_diff=np.array(current_meas)-np.array(x_med)
    sumQ=np.array(sumQ)+np.outer(aux_diff,aux_diff)
    #dt=t.to_nsec()-t_prev
    #t_prev=t.to_nsec()
    #periods.append(dt)
Q=sumQ/n
bagin.close() 
print(f"number of samples{n}")
'''

#linear_acc_cov=[q for line in Q for q in line]
variance_acc=1
variance_ang_vel=0.1
variance_orient=0.1
linear_acc_cov=[variance_acc, 0, 0,0,variance_acc,0,0,0,variance_acc]
ang_vel_cov=[variance_ang_vel,0,0,0,variance_ang_vel,0,0,0,variance_ang_vel]
orient_cov=[variance_orient,0,0,0,variance_orient,0,0,0,variance_orient]
bagin=rosbag.Bag(bagInName)
i=0
#print(f"bias {bias}")
for topic,msg,t in  bagin:
    i+=1
    '''if i<=10:
        print(msg.linear_acceleration)'''
    if(i==(n-1)/2 or i==n/2 or i==(n+1)/2):
        pass
        #print(f"measured acc while moving{msg.linear_acceleration}")
    '''if i>=n-10:
        print("-----")
        print(msg.linear_acceleration)'''
    msg.header.frame_id="pixhawk"
    msg.linear_acceleration.x-=bias[0]
    msg.linear_acceleration.y-=bias[1]

    """ 
    msg.linear_acceleration.x*=1
    msg.linear_acceleration.y*=1
    msg.linear_acceleration.z*=1
    msg.angular_velocity.y*=1
    msg.angular_velocity.z*=1
    msg.angular_velocity.x*=1
    """

    """
    accx=msg.linear_acceleration.x
    msg.linear_acceleration.x=msg.linear_acceleration.y
    msg.linear_acceleration.y=accx
    velx=msg.angular_velocity.x
    msg.angular_velocity.x=msg.angular_velocity.y
    msg.angular_velocity.y=velx
    msg.linear_acceleration.y*=-1
    msg.linear_acceleration.z*=-1
    msg.angular_velocity.y*=-1
    msg.angular_velocity.z*=-1
    """
    if(i==(n-1)/2 or i==n/2 or i==(n+1)/2):
        pass
        #print(f"measured acc while moving {msg.linear_acceleration}")
    msg.linear_acceleration_covariance=linear_acc_cov
    msg.angular_velocity_covariance=ang_vel_cov
    msg.orientation_covariance=orient_cov
    bagout.write(topic,msg,t)

#print(linear_acc_cov)
print(bagout.get_message_count())
print(i)
bagout.close()
bagin.close()


#print(np.multiply([1, 2, 3],[3, 4, 5]))
#print(np.array([1, 2, 3])+np.array([4, 5, 6]))
#print(np.array([1, 2, 3])/2)
#print(np.outer([1, 2, 3],[3, 4, 5,]))#a*b'
