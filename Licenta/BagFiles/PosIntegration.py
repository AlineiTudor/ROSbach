import rosbag
import numpy as np
import matplotlib.pyplot as plt

def read_acc(filename):
    acc=[[],[],[]]
    periods=[]
    bagin=rosbag.Bag(filename)
    first=True
    time=[]
    for topic,msg,t in bagin:
        acc[0].append(msg.linear_acceleration.x)
        acc[1].append(msg.linear_acceleration.y)
        acc[2].append(msg.linear_acceleration.z)
        time.append(t.to_nsec()/1000000000)
        if not first:
            dt=t.to_nsec()-t_prev
            periods.append(dt/1000000000)
        first=False
        t_prev=t.to_nsec()  
    bagin.close()
    return (acc,periods,time)

def filter(data,lamb=0.95):
    #data is a matrix
    length=len(data[0])
    dataout=np.zeros((3,length))
    print(dataout.shape)
    j=0
    for line in data:
        lineout=[]
        i=0
        for value in line:
            i+=1
            if i==1:
                filtered_val=(1-lamb)*value
            else:
                filtered_val=lamb*lineout[-1]+(1-lamb)*value
            lineout.append(filtered_val)
        dataout[j]=np.array(lineout)
        j+=1
    return list(dataout)

def trapz_integr(data,time_intervals):
    length=len(data[0])
    j=0
    dataout=np.zeros((3,length-1))
    for line in data:
        lineout=[]
        for i in range(len(line)-1):
            lineout.append((line[i]+line[i+1])/2*time_intervals[i])
        dataout[j]=np.array(lineout)
        j+=1
    return list(dataout)

def abs_val(pos):
    length=len(pos[0])
    j=0
    pos_abs_xyz=np.zeros((3,length))
    for line in pos:
        pos_abs=[]
        for i in range(len(line)):
            if i!=0:
                pos_abs.append(pos_abs[i-1]+line[i])
            else:
                pos_abs.append(0)
        pos_abs_xyz[j]=np.array(pos_abs)
        j+=1
    return list(pos_abs_xyz)
            
    

filename="/home/alineitudor/Licenta/BagFiles/Circle2Cov.bag"
acc,periods,time=read_acc(filename)
acc=filter(acc)
vel=trapz_integr(acc,periods)
vel=filter(vel)
vel_abs=abs_val(vel)
pos=trapz_integr(vel_abs,periods)
pos=filter(pos)
pos_abs=abs_val(pos)
print(f"position x {pos[0][1:10]}\n pos y {pos[1][0:10]}\n pos z {pos[2][0:10]}\n")
print(f"velocities x {vel[0][1:10]}\n velocities y {vel[1][0:10]}\n velocities z {vel[2][0:10]}\n")
print(f"acceleration x {acc[0][1:10]}\n acceleration y {acc[1][0:10]}\n acceleration z {acc[2][0:10]}\n time {periods[0:10]}")
#plt.plot(pos_abs[0],pos_abs[1])
plt.plot(time[0:len(time)-1],vel_abs[0],time[0:len(time)-1],vel_abs[1])
#plt.plot(time[0:len(time)-2],pos_abs[0],time[0:len(time)-2],pos_abs[1])
#plt.plot(periods)
plt.show()